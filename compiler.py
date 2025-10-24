"""
中文智能合约编译器主程序
整合词法分析、语法分析和代码生成
"""

import os
import sys
from typing import Optional

from lexer.chinese_lexer import ChineseLexer, tokenize
from parser.chinese_parser import ChineseParser, parse
from codegen.solidity_generator import SolidityGenerator, generate_solidity


class CompilerError(Exception):
    """编译器错误基类"""
    pass


class LexerError(CompilerError):
    """词法分析错误"""
    pass


class ParserError(CompilerError):
    """语法分析错误"""
    pass


class CodeGenError(CompilerError):
    """代码生成错误"""
    pass


class ChineseSolidityCompiler:
    """中文Solidity编译器"""
    
    def __init__(self, verbose: bool = False):
        """
        初始化编译器
        
        Args:
            verbose: 是否输出详细信息
        """
        self.verbose = verbose
        self.source_code = ""
        self.tokens = []
        self.ast = None
        self.solidity_code = ""
    
    def log(self, message: str):
        """输出日志信息"""
        if self.verbose:
            print(f"[编译器] {message}")
    
    def compile_file(self, input_file: str, output_file: Optional[str] = None) -> str:
        """
        编译中文智能合约文件
        
        Args:
            input_file: 输入文件路径（.zhs文件）
            output_file: 输出文件路径（.sol文件），如果为None则不写入文件
        
        Returns:
            生成的Solidity代码
        """
        self.log(f"读取源文件: {input_file}")
        
        # 读取源代码
        try:
            with open(input_file, 'r', encoding='utf-8') as f:
                self.source_code = f.read()
        except FileNotFoundError:
            raise CompilerError(f"文件不存在: {input_file}")
        except Exception as e:
            raise CompilerError(f"读取文件失败: {e}")
        
        # 编译
        solidity_code = self.compile(self.source_code)
        
        # 写入输出文件
        if output_file:
            self.log(f"写入输出文件: {output_file}")
            try:
                os.makedirs(os.path.dirname(output_file), exist_ok=True)
                with open(output_file, 'w', encoding='utf-8') as f:
                    f.write(solidity_code)
            except Exception as e:
                raise CompilerError(f"写入文件失败: {e}")
        
        return solidity_code
    
    def compile(self, source_code: str) -> str:
        """
        编译中文智能合约代码
        
        Args:
            source_code: 中文源代码
        
        Returns:
            生成的Solidity代码
        """
        self.source_code = source_code
        
        # 词法分析
        self.log("开始词法分析...")
        try:
            self.tokens = tokenize(source_code)
            self.log(f"词法分析完成，共 {len(self.tokens)} 个Token")
        except Exception as e:
            raise LexerError(f"词法分析失败: {e}")
        
        # 语法分析
        self.log("开始语法分析...")
        try:
            self.ast = parse(self.tokens)
            self.log("语法分析完成")
        except Exception as e:
            raise ParserError(f"语法分析失败: {e}")
        
        # 代码生成
        self.log("开始代码生成...")
        try:
            self.solidity_code = generate_solidity(self.ast)
            self.log("代码生成完成")
        except Exception as e:
            raise CodeGenError(f"代码生成失败: {e}")
        
        return self.solidity_code
    
    def get_tokens(self):
        """获取Token列表"""
        return self.tokens
    
    def get_ast(self):
        """获取AST"""
        return self.ast
    
    def get_solidity_code(self) -> str:
        """获取生成的Solidity代码"""
        return self.solidity_code


def compile_file(input_file: str, output_file: Optional[str] = None, verbose: bool = False) -> str:
    """
    便捷函数：编译中文智能合约文件
    
    Args:
        input_file: 输入文件路径
        output_file: 输出文件路径
        verbose: 是否输出详细信息
    
    Returns:
        生成的Solidity代码
    """
    compiler = ChineseSolidityCompiler(verbose=verbose)
    return compiler.compile_file(input_file, output_file)


def compile_code(source_code: str, verbose: bool = False) -> str:
    """
    便捷函数：编译中文智能合约代码
    
    Args:
        source_code: 中文源代码
        verbose: 是否输出详细信息
    
    Returns:
        生成的Solidity代码
    """
    compiler = ChineseSolidityCompiler(verbose=verbose)
    return compiler.compile(source_code)


if __name__ == "__main__":
    # 测试代码
    test_code = """
    合约 我的代币 {
        公开 字符串 名称 = "我的代币";
        公开 整数 总供应量;
        
        映射(地址 => 整数) 公开 余额;
        
        构造函数(整数 初始供应量) {
            总供应量 = 初始供应量;
            余额[消息发送者] = 初始供应量;
        }
        
        函数 转账(地址 接收者, 整数 金额) 公开 返回 布尔 {
            如果 (余额[消息发送者] >= 金额) {
                余额[消息发送者] -= 金额;
                余额[接收者] += 金额;
                返回 真;
            }
            返回 假;
        }
    }
    """
    
    print("=" * 60)
    print("中文智能合约编译器测试")
    print("=" * 60)
    print()
    
    print("中文源代码:")
    print("-" * 60)
    print(test_code)
    print()
    
    try:
        solidity_code = compile_code(test_code, verbose=True)
        print()
        print("生成的Solidity代码:")
        print("-" * 60)
        print(solidity_code)
    except CompilerError as e:
        print(f"编译失败: {e}")

