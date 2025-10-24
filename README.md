# 中文智能合约编译器 (Chinese Solidity Compiler)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)

一个支持使用中文语法编写智能合约的编译器，可以将中文代码编译为标准的 Solidity 代码，部署到 BSC（币安智能链）及其他 EVM 兼容链。

## ✨ 特性

- **🇨🇳 中文语法**：使用"合约"、"函数"、"整数"等中文关键字编写智能合约
- **🔄 即时编译**：自动将中文代码转换为标准 Solidity 代码
- **🎯 智能转换**：中文变量名自动转换为拼音，保留中文注释
- **📝 完整支持**：支持状态变量、函数、事件、require、emit 等常用功能
- **🌐 在线体验**：提供在线编译器，无需安装即可使用

## 🚀 快速开始

### 安装依赖

```bash
pip install pypinyin
```

### 编写第一个合约

创建 `hello.zhs` 文件：

```
合约 问候 {
    公开 字符串 消息 = "你好，世界！";
    
    函数 获取消息() 公开 只读 返回 字符串 {
        返回 消息;
    }
    
    函数 设置消息(字符串 新消息) 公开 {
        消息 = 新消息;
    }
}
```

### 编译合约

```python
from compiler import compile_file

# 编译文件
compile_file('hello.zhs', 'hello.sol', verbose=True)
```

生成的 Solidity 代码：

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract WenHou {
    string public XiaoXi = "你好，世界！";  // 消息
    
    function HuoQuXiaoXi() public view returns (string) {  // 获取消息
        return XiaoXi;
    }
    
    function SheZhiXiaoXi(string XinXiaoXi /* 新消息 */) public {  // 设置消息
        XiaoXi = XinXiaoXi;
    }
}
```

## 📚 语法说明

### 基本类型

| 中文 | Solidity | 说明 |
|------|----------|------|
| 整数 | uint256 | 无符号整数 |
| 有符号整数 | int256 | 有符号整数 |
| 地址 | address | 以太坊地址 |
| 布尔 | bool | 布尔值 |
| 字符串 | string | 字符串 |
| 字节 | bytes | 字节数组 |

### 关键字

| 中文 | Solidity | 说明 |
|------|----------|------|
| 合约 | contract | 合约定义 |
| 函数 | function | 函数定义 |
| 构造函数 | constructor | 构造函数 |
| 事件 | event | 事件定义 |
| 返回 | return | 返回语句 |
| 如果 | if | 条件语句 |
| 否则 | else | else 分支 |
| 循环 | for | for 循环 |
| 当 | while | while 循环 |
| 要求 | require | 条件检查 |
| 触发 | emit | 触发事件 |

### 可见性修饰符

| 中文 | Solidity |
|------|----------|
| 公开 | public |
| 私有 | private |
| 内部 | internal |
| 外部 | external |

### 状态可变性

| 中文 | Solidity |
|------|----------|
| 只读 | view |
| 纯函数 | pure |
| 可支付 | payable |

### 内置变量

| 中文 | Solidity |
|------|----------|
| 消息发送者 | msg.sender |
| 消息值 | msg.value |
| 区块号 | block.number |
| 区块时间 | block.timestamp |

## 📖 完整示例

### ERC20 代币合约

```
合约 我的代币 {
    公开 字符串 名称 = "我的代币";
    公开 整数 总供应量;
    
    映射(地址 => 整数) 公开 余额;
    
    事件 转账事件(地址 发送者, 地址 接收者, 整数 金额);
    
    构造函数(整数 初始供应量) {
        总供应量 = 初始供应量;
        余额[消息发送者] = 初始供应量;
    }
    
    函数 转账(地址 接收者, 整数 金额) 公开 返回 布尔 {
        要求(余额[消息发送者] >= 金额, "余额不足");
        
        余额[消息发送者] = 余额[消息发送者] - 金额;
        余额[接收者] = 余额[接收者] + 金额;
        
        触发 转账事件(消息发送者, 接收者, 金额);
        返回 真;
    }
}
```

## 🌐 在线编译器

访问在线编译器体验：[https://zhsc.niubiui.com](https://zhsc.niubiui.com)

## 🏗️ 项目结构

```
zhsc-compiler/
├── lexer/              # 词法分析器
│   └── chinese_lexer.py
├── parser/             # 语法分析器
│   └── chinese_parser.py
├── codegen/            # 代码生成器
│   └── solidity_generator.py
├── ast_nodes.py        # AST 节点定义
├── compiler.py         # 编译器主程序
└── examples/           # 示例合约
    ├── helloworld.zhs
    ├── token.zhs
    ├── voting.zhs
    └── auction.zhs
```

## 🔧 API 使用

### 编译代码字符串

```python
from compiler import compile_code

source_code = """
合约 测试 {
    公开 整数 数值 = 100;
}
"""

result = compile_code(source_code)
print(result)
```

### 编译文件

```python
from compiler import compile_file

compile_file('input.zhs', 'output.sol', verbose=True)
```

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📄 许可证

本项目采用 MIT 许可证。详见 [LICENSE](LICENSE) 文件。

## 🙏 致谢

- 感谢所有为区块链技术普及做出贡献的开发者
- 特别感谢 Solidity 和 BSC 社区

## 📮 联系方式

- 项目主页：[https://github.com/Anubisya/zhsc-compiler](https://github.com/Anubisya/zhsc-compiler)
- 在线编译器：[https://zhsc.niubiui.com](https://zhsc.niubiui.com)

---

**让智能合约开发更简单，让区块链技术更亲民！** 🚀

