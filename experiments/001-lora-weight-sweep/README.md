# Experiment 001: LoRA Weight Sweep

## Question

在固定 checkpoint、prompt、seed 和采样参数时，
LoRA 权重的变化会怎样影响生成结果？

我主要观察：

- 风格表现
- 人物结构
- 图像细节
- 伪影或过拟合痕迹

我考虑的目标lora是一个极富盛名的传奇lora——CunnyFunky

我将实验该lora在一张特定图里权重不同导致的变化

因此该实验实用意义并不高，仅作练习

## Hypothesis

我合理预测：

- 较低权重时，LoRA 风格不明显；
- 中等权重可能在风格与结构之间更平衡；
- 较高权重可能增强风格，也可能带来结构异常或细节粘连。

## Controlled Variables

- Checkpoint: chenkinNoobXLCKXL_v02
- 固定LoRA:略，详见测试图元信息
- 待测LORA:CunnyFunkyXLillokrV6311P
- Prompt: 略
- Negative prompt: 略
- Seed: 3820235668
- Sampler: DPM++ 2M Karras
- Steps: 35
- CFG: 7.0
- Resolution: 600x900

## Independent Variable

LoRA weight:

- 0.00
- 0.25
- 0.50
- 0.75
- 1.00

## Results

### Weight 0.00

![LoRA weight 0.00](../../assets/001-lora-weight-sweep/weight-0.00.png)

### Weight 0.25

![LoRA weight 0.25](../../assets/001-lora-weight-sweep/weight-0.25.png)

### Weight 0.50

![LoRA weight 0.50](../../assets/001-lora-weight-sweep/weight-0.50.png)

### Weight 0.75

![LoRA weight 0.75](../../assets/001-lora-weight-sweep/weight-0.75.png)

### Weight 1.00

![LoRA weight 1.00](../../assets/001-lora-weight-sweep/weight-1.00.png)

## Observations

## Observations

- Weight 0.00：几乎没有观察到目标 LoRA 的风格特征；由于本实验预先设计该lora为核心画风权重，因此缺失该lora之后图片质感较差，光效等都非常粗糙。
- Weight 0.25：开始出现一些目标风格的质感，但是由于权重较低，光效不足，画风质感依旧单薄粗糙。
- Weight 0.50：目标风格较明显，也很好的与其他lora相配合，美感得到质变。光效与灰度比例和谐，相得益彰，是在下最喜欢的一张
- Weight 0.75：cunnyfunky的独特画风开始凸显，光效润泽稍微溢出，一定程度上覆盖了其他lora，但由于cf的底子确实不错，所以美感还行。
- Weight 1.00：cf的风格彻底爆发，闪闪亮亮的灰润感极其凸出，但和其他lora的配合产生了一些失谐。

这只是一个固定 seed 下的观察，不足以说明某个权重普遍最优。

## Limitations

可想而知的局限性非常大

由于其他变量实在太多，因此本实验几乎不具备参考价值，权当练习

## Next Step

使用至少 3 个不同 seed 重复这组 LoRA 权重实验，
观察“中等权重更平衡”这一现象是否稳定。

后续可以尝试为每张图记录：

- 风格强度评分
- 人物结构评分
- 伪影程度评分