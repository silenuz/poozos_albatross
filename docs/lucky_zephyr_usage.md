The LuckyZephyr class can be used as a helper in querying the Doxygen XML for information regarding the project's source code.

## Variables

To query variables or methods, on can use the find methods in the LuckyZephyr class, these search for tag or attribute values in the
child elements and return the model of the parent node.  To help clarify this concept, here's the sample source code from the [Summator.h](../example/src/summator.h) file,
and the generated [XML](../example/doxygen_output/xml/classSummator.xml) for the first variable defined in the source code.

<table>
<tr>
<td><b>Summator Fields</b></td>
<td><b>Doxygen XML</b></td>
</tr>
<tr>
<td>

```cpp
/** The minimum total that is required to meet expenses */
static constexpr int MINMUM_REQUIRED_AMOUNT = 50;
/** Meeting expenses with a little extra */
static const int DOING_OKAY_AMOUNT = 100;
/** Things are going good, well into the black */
static const int DOING_NOTHING_AMOUNT = 200;
```

</td>
<td>

```xml
      <memberdef kind="variable" id="classSummator_1aa29ddd006b86446f127b8351be81a38b" prot="public" static="yes" constexpr="yes" mutable="no">
        <type>int</type>
        <definition>int Summator::MINMUM_REQUIRED_AMOUNT</definition>
        <argsstring></argsstring>
        <name>MINMUM_REQUIRED_AMOUNT</name>
        <qualifiedname>Summator::MINMUM_REQUIRED_AMOUNT</qualifiedname>
        <initializer>= 50</initializer>
        <briefdescription>
        </briefdescription>
        <detaileddescription>
            <para>The minimum total that is required to meet expenses </para>
        </detaileddescription>
        <inbodydescription>
        </inbodydescription>
        <location file="src/summator.h" line="84" column="22" bodyfile="src/summator.h" bodystart="84" bodyend="-1"/>
      </memberdef>
```

</td>
</tr>
</table>

For example if one wished to retrieve the model for the memberdef element of ```MINMUM_REQUIRED_AMOUNT```, based on the name
value:

```python
# fields and methods return member definitions
# look up constant value 'MINIMUM_REQUIRED_AMOUNT':
# field can be looked up by name:
lz = LuckyZephyr(summator_doxy_class_xml)
member_definition = lz.find_by_name('MINMUM_REQUIRED_AMOUNT')
print(f'\nConstant Details: "{member_definition.name}"')
print(f'Definition Kind: {member_definition.attributes.kind}')
print(f'Description: {member_definition.description}')
print(f'Type: {member_definition.type}')
print(f'Initial Value: {member_definition.initializer_value}')
```
Will result in this output:
```shell
Constant Details: "MINMUM_REQUIRED_AMOUNT"
Definition Kind: variable
Description: <para>The minimum total that is required to meet expenses </para>
Type: int
Initial Value: 50
```
