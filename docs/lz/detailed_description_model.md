
<a id="luckys_zephyr.DetailedDescriptionModel"></a>

## DetailedDescriptionModel Objects

```python
@dataclass()
class DetailedDescriptionModel()
```

Model to hold description information, with convenience properties to get the content as an element
or as plain text without html markup

<a id="luckys_zephyr.DetailedDescriptionModel.description"></a>

### description

detailed description of the method or member

<a id="luckys_zephyr.DetailedDescriptionModel.text_description"></a>

### text\_description

```python
@property
def text_description() -> str
```

Get the plain text (removes html markup) from the detaileddescription field


<a id="luckys_zephyr.DetailedDescriptionModel.node_description"></a>

### node\_description

```python
@property
def node_description() -> ElementTree.Element
```

Get the detailed description html and creates a node from it

**Returns**:

The node with the detailed description markup as the text