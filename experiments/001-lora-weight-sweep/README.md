# Experiment 001: LoRA Weight Sweep

## Question

在固定 checkpoint、prompt、seed 和采样参数时，
LoRA 权重的变化会怎样影响生成结果？

我主要观察：

- 风格表现
- 人物结构
- 图像细节
- 伪影或过拟合痕迹

## Hypothesis

我猜测：

- 较低权重时，LoRA 风格不明显；
- 中等权重可能在风格与结构之间更平衡；
- 较高权重可能增强风格，也可能带来结构异常或细节粘连。

## Controlled Variables

- Checkpoint: 待填写
- LoRA: 待填写
- Prompt: 待填写
- Negative prompt: 待填写
- Seed: 待填写
- Sampler: 待填写
- Steps: 待填写
- CFG: 待填写
- Resolution: 待填写

## Independent Variable

LoRA weight:

- 0.00
- 0.25
- 0.50
- 0.75
- 1.00

## Results

尚未完成。

## Observations

尚未完成。

## Limitations

目前尚未开始实验。

即使完成第一轮实验，若只使用一个 seed，
结论也只能视为一次观察，不能视为普遍规律。

## Next Step

选择一个已经安装好的 checkpoint 和一个非 NSFW 的 LoRA，
固定其余参数，只改变 LoRA 权重，生成五张对比图。