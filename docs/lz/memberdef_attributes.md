
<a id="luckys_zephyr.MemberDefinitionAttributes"></a>

## MemberDefinitionAttributes

```python
@dataclass(slots=True)
class MemberDefinitionAttributes()
```

Data model for Doxygen memberdef element attributes.

<a id="luckys_zephyr.MemberDefinitionAttributes.id"></a>

### id

A unique, auto-generated Doxygen identifier string used for cross-referencing throughout the XML structure

<a id="luckys_zephyr.MemberDefinitionAttributes.kind"></a>

### kind

Specifies the type of member. Common values include: function, variable, typedef, enum, enumvalue,
property, or event

<a id="luckys_zephyr.MemberDefinitionAttributes.prot"></a>

### prot

The access protection/visibility level in the source code. Possible values: public, protected, private,
or package

<a id="luckys_zephyr.MemberDefinitionAttributes.static"></a>

### static

Boolean indicator (yes or no) specifying if the member is declared static

<a id="luckys_zephyr.MemberDefinitionAttributes.const"></a>

### const

Boolean indicator (yes or no) showing if the member function acts as const

<a id="luckys_zephyr.MemberDefinitionAttributes.volatile"></a>

### volatile

Boolean indicator (yes or no) showing if the member is declared volatile

<a id="luckys_zephyr.MemberDefinitionAttributes.mutable"></a>

### mutable

Boolean indicator (yes or no) for C++ mutable variables

<a id="luckys_zephyr.MemberDefinitionAttributes.virt"></a>

### virt

Specifies virtual function behavior. Values: non-virtual, virtual, or pure-virtual.

<a id="luckys_zephyr.MemberDefinitionAttributes.explicit"></a>

### explicit

Boolean indicator (yes or no) for explicit C++ constructors/conversion operators

<a id="luckys_zephyr.MemberDefinitionAttributes.inline"></a>

### inline

Boolean indicator (yes or no) indicating if the member was defined inline

<a id="luckys_zephyr.MemberDefinitionAttributes.strong"></a>

### strong

Used primarily for scoping controls, such as C++ scoped enums (enum class) or C# strongly-typed data structures

<a id="luckys_zephyr.MemberDefinitionAttributes.extern"></a>

### extern

(Optional): Indicates if the variable or function is declared extern

<a id="luckys_zephyr.MemberDefinitionAttributes.refqual"></a>

### refqual

Identifies reference equality behavior, typically used when parsing managed languages like C# or CLI.

<a id="luckys_zephyr.MemberDefinitionAttributes.noexcept"></a>

### noexcept

Tracks whether a function or method is declared noexcept or has a non-throwing exception specification

<a id="luckys_zephyr.MemberDefinitionAttributes.noexceptexpression"></a>

### noexceptexpression

It captures the raw code snippet or conditional boolean logic passed inside a conditional noexcept(...) specifier

<a id="luckys_zephyr.MemberDefinitionAttributes.nodiscard"></a>

### nodiscard

Tracks the standard attribute [[nodiscard]] (found in C++17 and C23)

<a id="luckys_zephyr.MemberDefinitionAttributes.constexpr"></a>

### constexpr

Tracks if a function or variable is declared with the C++ constexpr specifier

<a id="luckys_zephyr.MemberDefinitionAttributes.consteval"></a>

### consteval

Tracks the C++20 consteval keyword

<a id="luckys_zephyr.MemberDefinitionAttributes.constinit"></a>

### constinit

Tracks the C++20 constinit keyword

<a id="luckys_zephyr.MemberDefinitionAttributes.settable"></a>

### settable

C++/CLI and C# property

<a id="luckys_zephyr.MemberDefinitionAttributes.privatesettable"></a>

### privatesettable

C++/CLI and C# property

<a id="luckys_zephyr.MemberDefinitionAttributes.protectedsettable"></a>

### protectedsettable

C++/CLI and C# property

<a id="luckys_zephyr.MemberDefinitionAttributes.gettable"></a>

### gettable

C++/CLI and C# property

<a id="luckys_zephyr.MemberDefinitionAttributes.privategettable"></a>

### privategettable

C++/CLI and C# property

<a id="luckys_zephyr.MemberDefinitionAttributes.protectedgettable"></a>

### protectedgettable

C++/CLI and C# property

<a id="luckys_zephyr.MemberDefinitionAttributes.final"></a>

### final

C++/CLI function

<a id="luckys_zephyr.MemberDefinitionAttributes.sealed"></a>

### sealed

C++/CLI function

<a id="luckys_zephyr.MemberDefinitionAttributes.new"></a>

### new

C++/CLI function

<a id="luckys_zephyr.MemberDefinitionAttributes.readable"></a>

### readable

Qt property

<a id="luckys_zephyr.MemberDefinitionAttributes.writable"></a>

### writable

Qt property

<a id="luckys_zephyr.MemberDefinitionAttributes.add"></a>

### add

C++/CLI event

<a id="luckys_zephyr.MemberDefinitionAttributes.remove"></a>

### remove

C++/CLI event

<a id="luckys_zephyr.MemberDefinitionAttributes.raise_"></a>

### raise\_

C++/CLI event

<a id="luckys_zephyr.MemberDefinitionAttributes.accessor"></a>

### accessor

Objective-C 2.0 property accessor

<a id="luckys_zephyr.MemberDefinitionAttributes.initonly"></a>

### initonly

C++/CLI variable