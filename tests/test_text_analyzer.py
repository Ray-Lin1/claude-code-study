"""
TextAnalyzer 类的单元测试
"""

from src.text_analyzer import TextAnalyzer


class TestTextAnalyzer:
    """TextAnalyzer 测试套件"""

    def test_word_count_simple_text(self):
        """测试简单文本的单词计数"""
        analyzer = TextAnalyzer("Hello world")
        assert analyzer.word_count() == 2

    def test_word_count_empty_string(self):
        """测试空字符串的单词计数"""
        analyzer = TextAnalyzer("")
        assert analyzer.word_count() == 0

    def test_word_count_multiple_spaces(self):
        """测试多个连续空格的单词计数"""
        analyzer = TextAnalyzer("Hello    world")
        assert analyzer.word_count() == 2

    def test_char_count_simple_text(self):
        """测试简单文本的字符计数（包含空格）"""
        analyzer = TextAnalyzer("Hello")
        assert analyzer.char_count() == 5

    def test_char_count_with_spaces(self):
        """测试包含空格的字符计数"""
        analyzer = TextAnalyzer("Hello world")
        assert analyzer.char_count() == 11  # "Hello" (5) + space (1) + "world" (5)

    def test_line_count_single_line(self):
        """测试单行文本的行数"""
        analyzer = TextAnalyzer("Hello world")
        assert analyzer.line_count() == 1

    def test_line_count_multiple_lines(self):
        """测试多行文本的行数"""
        analyzer = TextAnalyzer("Hello\nworld\nfoo")
        assert analyzer.line_count() == 3

    def test_line_count_empty_string(self):
        """测试空字符串的行数"""
        analyzer = TextAnalyzer("")
        assert analyzer.line_count() == 0

    def test_paragraph_count_single_paragraph(self):
        """测试单段落的段落数"""
        analyzer = TextAnalyzer("Hello world")
        assert analyzer.paragraph_count() == 1

    def test_paragraph_count_multiple_paragraphs(self):
        """测试多段落的段落数（由双换行符分隔）"""
        analyzer = TextAnalyzer("Hello\n\nWorld\n\nFoo")
        assert analyzer.paragraph_count() == 3

    def test_average_word_length(self):
        """测试平均单词长度"""
        analyzer = TextAnalyzer("Hello world")
        # Hello (5) + world (5) = 10 / 2 = 5.0
        assert analyzer.average_word_length() == 5.0

    def test_average_word_length_empty(self):
        """测试空文本的平均单词长度"""
        analyzer = TextAnalyzer("")
        assert analyzer.average_word_length() == 0.0

    def test_unicode_support(self):
        """测试 Unicode 字符支持"""
        analyzer = TextAnalyzer("Hello 世界")
        assert analyzer.word_count() == 2
        assert analyzer.char_count() == 8  # "Hello " (6) + "世界" (2)
