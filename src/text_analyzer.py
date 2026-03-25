"""
文本分析工具类

提供文本统计功能，包括单词数、字符数、行数、段落数和平均单词长度。
"""


class TextAnalyzer:
    """
    文本分析器

    提供多种文本统计方法，用于分析文本内容。

    Attributes:
        text (str): 要分析的文本内容

    Example:
        >>> analyzer = TextAnalyzer("Hello world")
        >>> analyzer.word_count()
        2
        >>> analyzer.char_count()
        11
    """

    def __init__(self, text: str) -> None:
        """
        初始化文本分析器

        Args:
            text: 要分析的文本内容
        """
        self.text = text

    def word_count(self) -> int:
        """
        统计文本中的单词数量

        单词由空格分隔，连续空格会被正确处理。

        Returns:
            单词数量

        Example:
            >>> analyzer = TextAnalyzer("Hello world")
            >>> analyzer.word_count()
            2
        """
        if not self.text.strip():
            return 0
        # 使用 split() 自动处理多个连续空格
        return len(self.text.split())

    def char_count(self) -> int:
        """
        统计文本中的字符数量（包含空格）

        Returns:
            字符总数

        Example:
            >>> analyzer = TextAnalyzer("Hello")
            >>> analyzer.char_count()
            5
        """
        return len(self.text)

    def line_count(self) -> int:
        """
        统计文本的行数

        Returns:
            行数（空文本返回 0）

        Example:
            >>> analyzer = TextAnalyzer("Hello\\nworld")
            >>> analyzer.line_count()
            2
        """
        if not self.text:
            return 0
        # splitlines() 正确处理各种换行符（\\n, \\r\\n, \\r）
        return len(self.text.splitlines())

    def paragraph_count(self) -> int:
        """
        统计文本的段落数

        段落由一个或多个换行符分隔。

        Returns:
            段落数

        Example:
            >>> analyzer = TextAnalyzer("Hello\\n\\nWorld")
            >>> analyzer.paragraph_count()
            2
        """
        if not self.text.strip():
            return 0
        # 按换行符分割，过滤空段落
        paragraphs = self.text.split("\n")
        non_empty = [p for p in paragraphs if p.strip()]
        return len(non_empty)

    def average_word_length(self) -> float:
        """
        计算文本中单词的平均长度

        Returns:
            平均单词长度（空文本返回 0.0）

        Example:
            >>> analyzer = TextAnalyzer("Hello world")
            >>> analyzer.average_word_length()
            5.0
        """
        words = self.text.split()
        if not words:
            return 0.0
        total_chars = sum(len(word) for word in words)
        return total_chars / len(words)
