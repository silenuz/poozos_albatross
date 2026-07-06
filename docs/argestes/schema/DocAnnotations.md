# DocAnnotations Schema:

```xml
<xs:element name="annotations" minOccurs="0">
    <xs:complexType>
        <xs:sequence>
            <xs:element name="annotation" maxOccurs="unbounded" minOccurs="0">
                <xs:complexType>
                    <xs:sequence>
                        <xs:element name="return" minOccurs="0">
                            <xs:complexType>
                                <xs:sequence>
                                    <xs:sequence/>
                                </xs:sequence>
                                <xs:attribute type="xs:string" name="type"/>
                                <xs:attribute type="xs:string" name="enum" use="optional"/>
                                <xs:attribute type="xs:boolean" name="is_bitfield" use="optional"/>
                            </xs:complexType>
                        </xs:element>
                        <xs:element name="param" maxOccurs="unbounded" minOccurs="0">
                            <xs:complexType>
                                <xs:sequence>
                                    <xs:sequence/>
                                </xs:sequence>
                                <xs:attribute type="xs:byte" name="index"/>
                                <xs:attribute type="xs:string" name="name"/>
                                <xs:attribute type="xs:string" name="type"/>
                                <xs:attribute type="xs:string" name="enum" use="optional"/>
                                <xs:attribute type="xs:boolean" name="is_bitfield" use="optional"/>
                                <xs:attribute type="xs:string" name="default" use="optional"/>
                            </xs:complexType>
                        </xs:element>
                        <xs:element type="xs:string" name="description"/>
                    </xs:sequence>
                    <xs:attribute type="xs:string" name="name" use="optional"/>
                    <xs:attribute type="xs:string" name="qualifiers" use="optional"/>
                    <xs:attribute type="xs:string" name="keywords" use="optional"/>
                </xs:complexType>
            </xs:element>
        </xs:sequence>
    </xs:complexType>
</xs:element>
```