# Transformer 零基础学习指南

从“Transformer 为什么出现”开始，用背景、比喻、手算和完整例子，理解一句话怎样变成数字，Attention 怎样计算，以及模型怎样训练和生成文本。

**完整文档：[Transformer 零基础学习指南](docs/Transformer-零基础学习指南.md)**

适合第一次学习 Transformer 的读者。不要求先掌握机器学习或高等数学。

文档包含：

- 前因后果：从规则系统、RNN 的困难讲到 Attention 与 Transformer。
- 核心原理：token、embedding、位置、多头注意力、FFN、残差与归一化。
- 完整流程：Encoder/Decoder、预测下一个 token、训练、生成与上下文。
- 手算、无需 GPU 的小实验、常见误解、术语解释和分阶段学习路线。

GPU 与 Kubernetes 只在文末作简短联系，正文集中讲 Transformer。

建议第一遍先看故事和例子，第二遍做 Attention 手算与实验，第三遍尝试自己解释一次完整流程。
