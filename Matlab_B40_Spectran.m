%% USRP B210 接收星座图 + 频谱 + EVM 
% 作者: 0xroot
% 日期: 2025年4月
% 功能: 接收64QAM/256QAM信号，实时绘制星座图、频谱图、计算EVM，可动态调整中心频率
clear; clc; close all;
%% 用户设置区域
modType = '64QAM';    % 选择 '64QAM' 或 '256QAM'
initCenterFreq = 2.33e9; % 初始中心频率2330MHz
deviceSerial = '';    % ⚡ 如果知道B210序列号，写进去；否则留空自动搜索
maxSafeSamples = 20000;  % 每帧样本数，防止Symbol同步器爆掉
%% 加载参考星座图
switch modType
    case '64QAM'
        M = 64;
    case '256QAM'
        M = 256;
    otherwise
        error('❌ 不支持的调制类型，请选择 ''64QAM'' 或 ''256QAM''');
end
refSymbols = qammod(0:M-1, M, 'UnitAveragePower', true);
%% 检查B210设备连接
disp('🔍 正在查找USRP设备...');
hw = findsdru;
if strcmp(hw.Status, 'Success')
    disp(['✅ 找到设备，序列号: ' hw.SerialNum]);
else
    error('❌ 没有找到可用的USRP B210设备，请检查连接');
end
%% 初始化B210
radio = comm.SDRuReceiver(...
    'Platform', 'B200', ...
    'CenterFrequency', initCenterFreq, ...
    'Gain', 30, ...
    'SamplesPerFrame', maxSafeSamples, ... % ✅ 修正！防止溢出
    'MasterClockRate', 20e6, ...
    'DecimationFactor', 1, ...
    'OutputDataType', 'double');
if ~isempty(deviceSerial)
    radio.SerialNum = deviceSerial;
else
    radio.SerialNum = hw.SerialNum;
end
%% 建立同步器和可视化器
timingRecovery = comm.SymbolSynchronizer(...
    'TimingErrorDetector', 'Gardner (non-data-aided)', ...
    'SamplesPerSymbol', 2, ...
    'DampingFactor', 1, ...
    'NormalizedLoopBandwidth', 0.01);
carrierRecovery = comm.CarrierSynchronizer(...
    'SamplesPerSymbol', 1, ...
    'DampingFactor', 0.707, ...
    'NormalizedLoopBandwidth', 0.001);
constDiagram = comm.ConstellationDiagram(...
    'SamplesPerSymbol', 1, ...
    'ReferenceConstellation', refSymbols, ...
    'Title', ['USRP B210 星座图 - ' modType], ...
    'ShowTrajectory', false, ...
    'XLimits', [-2 2], ...
    'YLimits', [-2 2]);
spectrumAnalyzer = dsp.SpectrumAnalyzer(...
    'SampleRate', 20e6, ...
    'ShowLegend', true, ...
    'Title', 'USRP B210 实时频谱');
disp('✅ USRP B210接收器初始化完成');
disp('✅ 按Ctrl+C停止程序，或输入新频率或q退出');
lastPromptTime = tic;  % 记录上次询问时间
%% 主接收循环
frameCount = 0;  % 帧计数器
while true
    [rxData, dataLen] = radio();
    if dataLen > 0
        frameCount = frameCount + 1;
        rxPower = 10*log10(mean(abs(rxData).^2) + eps);
        fprintf('帧 %d: 接收长度: %d, 功率: %.2f dB\n', frameCount, dataLen, rxPower);
        % 同步处理
        try
            syncData = timingRecovery(rxData);
            syncData = carrierRecovery(syncData);
        catch ME
            warning('⚠️ 同步处理异常: %s，跳过本帧', ME.message);
            continue;
        end
        % 绘制星座图
        constDiagram(syncData);
        % 绘制频谱图
        spectrumAnalyzer(rxData);
        % 计算并显示EVM
        demodData = qamdemod(syncData, M, 'UnitAveragePower', true);
        remodData = qammod(demodData, M, 'UnitAveragePower', true);
        evm = sqrt(mean(abs(syncData - remodData).^2)) * 100; % 单帧EVM(%)
        fprintf('当前EVM: %.2f %%\n', evm);
    end
    % 每5秒询问是否需要调整频率
    if toc(lastPromptTime) > 5
        userInput = input('输入新中心频率 (Hz)，回车保持，q退出: ', 's');
        lastPromptTime = tic;  % 重新计时
        if strcmpi(userInput, 'q')
            disp('🛑 用户选择退出...');
            break;
        elseif ~isempty(userInput)
            newFreq = str2double(userInput);
            if ~isnan(newFreq) && newFreq > 0
                radio.CenterFrequency = newFreq;
                fprintf('✔ 中心频率调整到 %.3f MHz\n', newFreq/1e6);
            else
                disp('⚠️ 无效输入，保持当前频率');
            end
        end
    end
end
%% 清理资源
release(radio);
release(constDiagram);
release(spectrumAnalyzer);
disp('✅ 已释放USRP资源，程序结束。');
