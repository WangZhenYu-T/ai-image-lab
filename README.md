# AI Image Lab

这是我的生成式图像实验仓库。

这里不用于收集模型资讯，也不用于堆放未经验证的代码。
每个实验尽量包含：

1. 一个明确的问题
2. 固定或记录过的实验配置
3. 控制变量
4. 实验结果
5. 观察、失败和局限
6. 下一步问题

## Current Experiment

- [001: LoRA Weight Sweep](./experiments/001-lora-weight-sweep/)

## Utilities

Generate a labeled comparison grid from an image folder:

```powershell
python scripts/make_grid.py --input assets/001-lora-weight-sweep --output assets/001-lora-weight-sweep/grid.jpg --columns 5 --cell-width 300
```
