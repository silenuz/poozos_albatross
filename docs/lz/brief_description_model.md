
<a id="luckys_zephyr.BriefDescriptionModel"></a>

## BriefDescriptionModel Objects

```python
@dataclass()
class BriefDescriptionModel()
```

<a id="luckys_zephyr.BriefDescriptionModel.briefdescription"></a>

### briefdescription

description of the method or member

<a id="luckys_zephyr.BriefDescriptionModel.text_brief_description"></a>

### text\_brief\_description

```python
@property
def text_brief_description() -> str
```

Get the plain text (removes html markup) from the brief description field


<a id="luckys_zephyr.BriefDescriptionModel.node_brief_description"></a>

### node\_brief\_description

```python
@property
def node_brief_description() -> ElementTree.Element
```

Get the brief description html and creates a node from it

**Returns**:

The node with the briefdescription markup as the text