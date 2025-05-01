# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.6.x] - 2025-04-16

### Added

- 新增管理页面 (管理员面板-设置-积分)
- 新增报表页面 (管理员面板-用户-积分统计)
- 支持配置积分兑换比例 (用于充值折扣)
- 支持对特性按次计费 (如网页搜索、图片生成)
- 支持配置请求模型需要的最低余额
- 工作空间中配置的模型使用基础模型价格计费
- 支持配置用户的初始积分
- 模型选项增加模型价格提示
- 支持对 Ollama 模型计费

### Changed

- 优化 Usage 兼容性
- 优化积分日志内容
- 优化充值二维码展示效果
- 优化响应数据的 Usage 格式
- 优化初始积分的小数位数
- 优化免费请求的积分余额校验
- 优化 Token 计算精确度

### Fixed

- 修复易支付的兼容问题
- 修复调用 chat.completion api 的兼容问题

## [0.6.5.16] - 2025-04-16

### Added

- 支持按照请求次数计费
- 支持 Pipe 模型计费
- 在对话 Usage 中增加扣费信息
- 增加 Markdown 编辑器
- 增加代码块折叠功能
- 支持通过 API 批量修改模型价格
- 支持设置允许充值的金额范围

### Changed

- 优化易支付支付后的跳转
- 优化较长上下文的计算性能

### Fixed

- 修复支付连接无法在微信内置浏览器打开的问题
- 修复余额不足的异常没有保存到对话日志的问题

## [0.6.4.9] - 2025-04-16

### Added

- 支持配置模型价格
- 支持用户充值积分 (易支付)

## [0.6.4.1] - 2025-04-13

### Added

- 支持自定义 Logo & Title
