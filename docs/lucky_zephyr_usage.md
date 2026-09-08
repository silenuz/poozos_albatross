The LuckyZephyr class can be used as a helper in querying the Doxygen XML for information regarding the project's source code.

## Variables

To query variables or methods, on can use the find methods in the LuckyZephyr class, these search for tag or attribute values in the
child elements and return the model of the parent node.  To help clarify this concept, here's the sample source code from the [Summator.h](../example/src/summator.h) file,
and the generated [XML](../example/doxygen_output/xml/classSummator.xml) for the first variable defined in the source code.

Summator Code:
```cpp
/** The minimum total that is required to meet expenses */
static constexpr int MINMUM_REQUIRED_AMOUNT = 50;
/** Meeting expenses with a little extra */
static const int DOING_OKAY_AMOUNT = 100;
/** Things are going good, well into the black */
static const int DOING_NOTHING_AMOUNT = 200;
```

Generated XML:

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

## Methods

Like variables methods can be found using the name, or qualified name, of the method.  

### Method Return Value

In many instances it may be desirable to have information about a methods's return value.
To demonstrate this concept, in the next example the method name is used to retrieve data about the ```get_total()``` method in the Summator class.
Some of the attributes are then printed out, including the return value type and description of the return value.

Summator Source:

```cpp
	/**
	 * @brief returns the current total
	 *
	 * This function returns the current total, which is the sum of all the integers
	 * the summator added together.
	 *
	 * @return the sum of all the integers that were added together
	 */
	int get_total() const;
```

Generated XML:

```xml
      <memberdef kind="function" id="classSummator_1a1c3b1b74ac163588a654900ec500685c" prot="public" static="no" const="yes" explicit="no" inline="no" virt="non-virtual">
        <type>int</type>
        <definition>int Summator::get_total</definition>
        <argsstring>() const</argsstring>
        <name>get_total</name>
        <qualifiedname>Summator::get_total</qualifiedname>
        <briefdescription>
            <para>returns the current total </para>
        </briefdescription>
        <detaileddescription>
            <para>This function returns the current total, which is the sum of all the integers the summator added together.</para>
            <para>
            <simplesect kind="return">
                <para>the sum of all the integers that were added together </para>
            </simplesect>
        </para>
        </detaileddescription>
        <inbodydescription>
        </inbodydescription>
        <location file="src/summator.h" line="115" column="5" bodyfile="src/summator.cpp" bodystart="38" bodyend="40"/>
      </memberdef>
```

Sample:

```python
lz = LuckyZephyr(summator_doxy_class_xml)
# lookup method by name and print some attributes
member_definition = lz.find_by_name('get_total')
print(f'\nMethod Details: "{member_definition.name}"')
print(f'Definition Kind: {member_definition.attributes.kind}')
print(f'Brief: {member_definition.briefdescription}')
print(f'Description: {member_definition.description}')
# print return type and description
print(f'Return Type: {member_definition.type}')
# doxygen xml
print(f'return description: {member_definition.returns.description}')
# plain text
print(f'return description plain text: {member_definition.returns.text_description}')
# get the file that contains the definition
print(f'File: {member_definition.location.file}')
# get the file contains the implementation
print(f'Implementation: {member_definition.location.bodyfile}')
```
Output:

```shell
Method Details: "get_total"
Definition Kind: function
Brief: <para>returns the current total </para>
Description: <para>This function returns the current total, which is the sum of all the integers the summator added together.</para>
Return Type: int
return description: <para>the sum of all the integers that were added together </para>
return description plain text: the sum of all the integers that were added together 
File: src/summator.h
Implementation: src/summator.cpp
```

### Method Args

In many instances it may be desirable to have information about a methods's parameters.
To demonstrate this concept, in the next example the method's qualified name is used to retrieve data about 
the ```add()``` method in the Summator class.
Some of the attributes are then printed out, including parameter types and descriptions.

Summator Code:

```cpp
	/**
	 * @brief adds the passed value to the current total
	 *
	 * This function simply adds the integer value of the argument to the current total
	 *
	 * @param p_value integer value to be added to the current total
	 *
	 * */
	void add(int p_value);
```

Generated XML:

```xml
<memberdef kind="function" id="classSummator_1a6294425c68c6937d4de8cc2334069b00" prot="public" static="no" const="no" explicit="no" inline="no" virt="non-virtual">
    <type>void</type>
    <definition>void Summator::add</definition>
    <argsstring>(int p_value)</argsstring>
    <name>add</name>
    <qualifiedname>Summator::add</qualifiedname>
    <param>
        <type>int</type>
        <declname>p_value</declname>
    </param>
    <briefdescription>
        <para>adds the passed value to the current total </para>
    </briefdescription>
    <detaileddescription>
        <para>This function simply adds the integer value of the argument to the current total</para>
        <para><parameterlist kind="param"><parameteritem>
                    <parameternamelist>
                        <parametername>p_value</parametername>
                    </parameternamelist>
                    <parameterdescription>
                        <para>integer value to be added to the current total </para>
                    </parameterdescription>
                </parameteritem>
            </parameterlist>
        </para>
    </detaileddescription>
    <inbodydescription>
    </inbodydescription>
    <location file="src/summator.h" line="98" column="6" bodyfile="src/summator.cpp" bodystart="29" bodyend="32"/>
</memberdef>
```

Sample:

```python
lz = LuckyZephyr(summator_doxy_class_xml)
# use qualified name to look up method and print some attributes:
member_definition = lz.find_by_qualified('Summator::add')
print(f'\nMethod Details: "{member_definition.name}"')
print(f'Kind: {member_definition.attributes.kind}')
print(f'Protection: {member_definition.attributes.prot}')
print(f'ID: {member_definition.attributes.id}')
# plain text
print(f'Brief (Plain): {member_definition.text_brief_description}')
print(f'Description (Plain): {member_definition.text_description}')

# handling arg string and parameters
print(f'args: {member_definition.argsstring}')
for parameter in member_definition.parameters:
    print(f'\tParameter: {parameter.declname}')
    print(f'\tType: {parameter.type}')
    print(f'\tDescription: {parameter.description}')
```
Output:

```shell
Method Details: "add"
Kind: function
Protection: public
ID: classSummator_1a6294425c68c6937d4de8cc2334069b00
Brief (Plain): adds the passed value to the current total 
Description (Plain): This function simply adds the integer value of the argument to the current total
args: (int p_value)
	Parameter: p_value
	Type: int
	Description: <para>integer value to be added to the current total </para>
```