%% USRP B210接收星座图 + 频谱 + EVM 
% 作者: 0xroot
% 日期: 2025年4月
% 功能: 接收64QAM/256QAM信号，实时显示星座图、频谱、EVM，支持动态调频。
clear; clc; close all;
%% 用户设置
modType = '64QAM';          % '64QAM' 或 '256QAM'
initCenterFreq = 1.85e9;     % 初始中心频率 1850MHz
deviceSerial = '';           % B210序列号 (可留空)
sampleRate = 20e6;           % 采样率20MHz
samplesPerFrame = 40000;     % 每帧采样数
gain = 30;                   % 接收增益
symbolRate = 10e6;           % 符号率10MHz (适配64QAM/256QAM)
%% 加载参考星座图
switch modType
    case '64QAM'
        M = 64;
    case '256QAM'
        M = 256;
    otherwise
        error('不支持的调制方式，请选择 ''64QAM'' 或 ''256QAM''');
end
refConst = qammod(0:M-1, M, 'UnitAveragePower', true);
%% 查找设备
disp('🔍 正在查找USRP设备...');
hw = findsdru;
if strcmp(hw.Status, 'Success')
    disp(['✅ 找到设备，序列号: ' hw.SerialNum]);
else
    error('❌ 没找到USRP B210设备，请检查连接');
end
%% 创建接收对象
radio = comm.SDRuReceiver(...
    'Platform', 'B200', ...
    'CenterFrequency', initCenterFreq, ...
    'Gain', gain, ...
    'SamplesPerFrame', samplesPerFrame, ...
    'MasterClockRate', sampleRate, ...
    'DecimationFactor', 1, ...
    'OutputDataType', 'double');
if ~isempty(deviceSerial)
    radio.SerialNum = deviceSerial;
else
    radio.SerialNum = hw.SerialNum;
end
%% 创建同步器、可视化器
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
    'ReferenceConstellation', refConst, ...
    'SamplesPerSymbol', 1, ...
    'ShowTrajectory', false, ...
    'Title', ['USRP B210 星座图 - ' modType], ...
    'XLimits', [-2 2], ...
    'YLimits', [-2 2]);
spectrumAnalyzer = dsp.SpectrumAnalyzer(...
    'SampleRate', sampleRate, ...
    'Title', 'USRP B210 实时频谱', ...
    'ShowLegend', true);
evmPlot = animatedline('Color', 'r', 'LineWidth', 2);
figure('Name','EVM (%) 曲线','NumberTitle','off');
grid on; xlabel('时间 (帧数)'); ylabel('EVM (%)'); title('实时EVM曲线');
ylim([0 20]);
frameCount = 0;
% 创建主控制窗口
hFig = figure('Name','USRP接收控制窗口','NumberTitle','off');
set(hFig, 'KeyPressFcn', @(src,event)setappdata(src,'keypressed',event.Key));
setappdata(hFig, 'keypressed', '');
disp('✅ USRP B210接收器初始化完成');
disp('✅ 按"q"退出程序，按"f"动态调频');
%% 主循环
exitFlag = false;
lastPromptTime = tic;
while ~exitFlag && ishandle(hFig)
    [rxData, dataLen] = radio();
    if dataLen > 0
        rxPower = 10*log10(mean(abs(rxData).^2) + eps);
        fprintf('帧 %d: 接收长度: %d, 功率: %.2f dB\n', frameCount, dataLen, rxPower);
        % 同步
        syncData = timingRecovery(rxData);
        syncData = carrierRecovery(syncData);
        % 星座图
        constDiagram(syncData);
        % 频谱
        spectrumAnalyzer(rxData);
        % EVM计算
        demodData = qamdemod(syncData, M, 'UnitAveragePower', true);
        remodData = qammod(demodData, M, 'UnitAveragePower', true);
        evmVal = sqrt(mean(abs(syncData - remodData).^2)) * 100;  % 百分比
        frameCount = frameCount + 1;
        addpoints(evmPlot, frameCount, evmVal);
        drawnow limitrate;
        fprintf('当前EVM: %.2f %%\n', evmVal);
    end
    % 键盘输入检测
    key = getappdata(hFig, 'keypressed');
    if ~isempty(key)
        if strcmpi(key, 'q')
            disp('🛑 用户退出');
            exitFlag = true;
        elseif strcmpi(key, 'f')
            newFreq = input('请输入新中心频率 (Hz): ');
            if isnumeric(newFreq) && ~isnan(newFreq) && newFreq>0
                radio.CenterFrequency = newFreq;
                fprintf('✔ 中心频率切换到 %.3f MHz\n', newFreq/1e6);
            else
                disp('⚠️ 输入无效');
            end
        end
        setappdata(hFig, 'keypressed', '');
    end
end
%% 释放资源
release(radio);
release(constDiagram);
release(spectrumAnalyzer);
disp('✅ 资源释放完成，程序退出');
