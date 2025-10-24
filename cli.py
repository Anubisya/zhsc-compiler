#!/usr/bin/env python3
"""
中文智能合约编译器命令行工具
"""

import os
import sys
import click
from rich.console import Console
from rich.syntax import Syntax
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn

from compiler import ChineseSolidityCompiler, CompilerError

console = Console()


@click.group()
@click.version_option(version="0.1.0")
def cli():
    """中文智能合约编译器 (Chinese Solidity Compiler)
    
    使用中文语法编写智能合约，编译为Solidity代码并部署到BSC链。
    """
    pass


@cli.command()
@click.argument('input_file', type=click.Path(exists=True))
@click.option('-o', '--output', 'output_file', type=click.Path(), help='输出文件路径')
@click.option('-v', '--verbose', is_flag=True, help='显示详细信息')
@click.option('--show-tokens', is_flag=True, help='显示Token列表')
@click.option('--show-ast', is_flag=True, help='显示AST')
def compile(input_file, output_file, verbose, show_tokens, show_ast):
    """编译中文智能合约文件
    
    示例:
        zhsc compile my_contract.zhs -o my_contract.sol
    """
    try:
        # 如果没有指定输出文件，自动生成
        if not output_file:
            base_name = os.path.splitext(input_file)[0]
            output_file = base_name + '.sol'
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
            transient=True
        ) as progress:
            task = progress.add_task("正在编译...", total=None)
            
            # 创建编译器
            compiler = ChineseSolidityCompiler(verbose=verbose)
            
            # 编译文件
            solidity_code = compiler.compile_file(input_file, output_file)
            
            progress.update(task, completed=True)
        
        # 显示Token列表
        if show_tokens:
            console.print("\n[bold cyan]Token列表:[/bold cyan]")
            for i, token in enumerate(compiler.get_tokens()[:20]):  # 只显示前20个
                console.print(f"  {i+1}. {token}")
            if len(compiler.get_tokens()) > 20:
                console.print(f"  ... 还有 {len(compiler.get_tokens()) - 20} 个Token")
        
        # 显示AST
        if show_ast:
            console.print("\n[bold cyan]抽象语法树(AST):[/bold cyan]")
            console.print(compiler.get_ast())
        
        # 显示生成的代码
        console.print("\n[bold green]✓ 编译成功![/bold green]")
        console.print(f"输入文件: {input_file}")
        console.print(f"输出文件: {output_file}")
        
        # 显示生成的Solidity代码
        console.print("\n[bold cyan]生成的Solidity代码:[/bold cyan]")
        syntax = Syntax(solidity_code, "solidity", theme="monokai", line_numbers=True)
        console.print(Panel(syntax, title="Solidity代码", border_style="green"))
        
    except CompilerError as e:
        console.print(f"\n[bold red]✗ 编译失败:[/bold red] {e}", style="red")
        sys.exit(1)
    except Exception as e:
        console.print(f"\n[bold red]✗ 错误:[/bold red] {e}", style="red")
        sys.exit(1)


@cli.command()
@click.argument('input_file', type=click.Path(exists=True))
def check(input_file):
    """检查中文智能合约语法
    
    示例:
        zhsc check my_contract.zhs
    """
    try:
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
            transient=True
        ) as progress:
            task = progress.add_task("正在检查语法...", total=None)
            
            # 创建编译器
            compiler = ChineseSolidityCompiler(verbose=False)
            
            # 读取源代码
            with open(input_file, 'r', encoding='utf-8') as f:
                source_code = f.read()
            
            # 编译（不输出文件）
            compiler.compile(source_code)
            
            progress.update(task, completed=True)
        
        console.print(f"\n[bold green]✓ 语法检查通过![/bold green]")
        console.print(f"文件: {input_file}")
        
    except CompilerError as e:
        console.print(f"\n[bold red]✗ 语法错误:[/bold red] {e}", style="red")
        sys.exit(1)
    except Exception as e:
        console.print(f"\n[bold red]✗ 错误:[/bold red] {e}", style="red")
        sys.exit(1)


@cli.command()
def version():
    """显示版本信息"""
    console.print("[bold cyan]中文智能合约编译器[/bold cyan]")
    console.print("版本: 0.1.0")
    console.print("作者: Your Name")
    console.print("许可证: MIT")


@cli.command()
def examples():
    """显示示例代码"""
    example_code = """合约 我的代币 {
    公开 字符串 名称 = "我的代币";
    公开 字符串 符号 = "MYT";
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
    
    函数 查询余额(地址 账户) 公开 只读 返回 整数 {
        返回 余额[账户];
    }
}"""
    
    console.print("\n[bold cyan]示例：ERC20代币合约[/bold cyan]\n")
    syntax = Syntax(example_code, "text", theme="monokai", line_numbers=True)
    console.print(Panel(syntax, title="中文智能合约示例", border_style="cyan"))
    
    console.print("\n[bold yellow]编译命令:[/bold yellow]")
    console.print("  zhsc compile token.zhs -o token.sol")


def main():
    """主函数"""
    try:
        cli()
    except KeyboardInterrupt:
        console.print("\n\n[yellow]操作已取消[/yellow]")
        sys.exit(0)
    except Exception as e:
        console.print(f"\n[bold red]错误:[/bold red] {e}", style="red")
        sys.exit(1)


if __name__ == "__main__":
    main()

