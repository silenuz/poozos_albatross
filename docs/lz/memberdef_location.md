
<a id="luckys_zephyr.MemberDefinitionLocation"></a>

## MemberDefinitionLocation

```python
@dataclass(slots=True)
class MemberDefinitionLocation()
```

<a id="luckys_zephyr.MemberDefinitionLocation.file"></a>

### file

The path to the source file where the member is defined or declared.
This is usually relative to the root input directory unless full paths are enabled in your Doxyfile.

<a id="luckys_zephyr.MemberDefinitionLocation.line"></a>

### line

The line number in the source file where the member's definition or declaration begins.

<a id="luckys_zephyr.MemberDefinitionLocation.column"></a>

### column

The column number (character offset) on the line where the member begins.
(Note: column reporting can be dependent on your specific Doxygen version and configuration).

<a id="luckys_zephyr.MemberDefinitionLocation.bodyfile"></a>

### bodyfile

The path to the source file where the actual body (implementation) of the member resides.
This is typically used for functions or methods, whereas file denotes where the signature is declared.

<a id="luckys_zephyr.MemberDefinitionLocation.bodystart"></a>

### bodystart

The line number where the implementation of the member starts (e.g., the opening brace of a function).

<a id="luckys_zephyr.MemberDefinitionLocation.bodyend"></a>

### bodyend

The line number where the implementation of the member ends (e.g., the closing brace of a function).