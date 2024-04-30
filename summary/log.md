```shell
# 静态查看GPU使用情况
nvidia-smi
# 以T为周期查看GPU使用情况：watch -n T nvidia-smi
# 注意：命令行参数T表示执行命令的周期(单位：S)
watch -n 30 nvidia-smi
# 查看服务器是64位还是32位
getconf LONG_BIT
```
```text
表头释义： 

Fan：显示风扇转速，数值在0到100%之间，是计算机的期望转速，如果计算机不是通过风扇冷却或者风扇坏了，显示出来就是N/A； 
Temp：显卡内部的温度，单位是摄氏度；
Perf：表征性能状态，从P0到P12，P0表示最大性能，P12表示状态最小性能；
Pwr：能耗表示； 
Bus-Id：涉及GPU总线的相关信息； 
Disp.A：是Display Active的意思，表示GPU的显示是否初始化； 
Memory Usage：显存的使用率； 
Volatile GPU-Util：浮动的GPU利用率；
Compute M：计算模式； 
+---------------------------------------------------------------------------------------+
| NVIDIA-SMI 535.113.01             Driver Version: 535.113.01   CUDA Version: 12.2     |
|-----------------------------------------+----------------------+----------------------+
| GPU  Name                 Persistence-M | Bus-Id        Disp.A | Volatile Uncorr. ECC |
| Fan  Temp   Perf          Pwr:Usage/Cap |         Memory-Usage | GPU-Util  Compute M. |
|                                         |                      |               MIG M. |
|=========================================+======================+======================|
|   0  NVIDIA GeForce RTX 4090        Off | 00000000:01:00.0 Off |                  Off |
|  0%   40C    P8              10W / 450W |   1819MiB / 24564MiB |      0%      Default |
|                                         |                      |                  N/A |
+-----------------------------------------+----------------------+----------------------+
                                                                                         
+---------------------------------------------------------------------------------------+
| Processes:                                                                            |
|  GPU   GI   CI        PID   Type   Process name                            GPU Memory |
|        ID   ID                                                             Usage      |
|=======================================================================================|
|    0   N/A  N/A      2124      G   /usr/libexec/Xorg                            15MiB |
|    0   N/A  N/A    256081      C   /usr/local/bin/python                      1788MiB |
+---------------------------------------------------------------------------------------+
```

conda环境创建使用
```shell
conda create -n mySummary python=3.11
source activate mySummary
```
