import warnings
import string


# 用 PartialDict 保留未填充的字段
class PartialDict(dict):
    def __missing__(self, key):
        return '{' + key + '}'

formatter = string.Formatter()

class StringTemplate:
        
    @property
    def Content(self) -> str:
        """返回当前字符串，未填充的字段用<xxx>表示"""
        x = self._current
        for _, field_name, _, _ in formatter.parse(x):
            if field_name is not None:
                x = x.replace(f'{{{field_name}}}', f'<{field_name}>')
        return x
    
    def __init__(self, template: str):
        self._template = template
        self._current = template

    def format(self, **kwargs: dict) -> 'StringTemplate':
        """分批次填充"""
        self._current = self._current.format_map(PartialDict(**kwargs))
        return self

    def __str__(self) -> str:
        """返回当前字符串"""
        if self._has_unfilled():
            warnings.warn(f"StringFormatter warning: still has unfilled placeholders in '{self._current}'")
        return self._current

    def _has_unfilled(self):
        """检查还有没有 {xxx} 占位符"""
        for _, field_name, _, _ in formatter.parse(self._current):
            if field_name is not None:
                return True
        return False

    def reset(self) -> 'StringTemplate':
        """重置回最初的模板"""
        self._current = self._template
        return self
