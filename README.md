# ptmod: Modify PyTorch model
Command line utilies to modify serialized pytorch model states.

## The definition of pytorch model file
In the context of this text, a model file should be a serialized `state_dict` object. See for mote detail: https://pytorch.org/docs/stable/notes/serialization.html

```python
# e.g.
import torch

class Block(torch.nn.Module):
    def __init__(self):
        super().__init__()
        self.layer1 = torch.nn.Linear(10, 10)
        self.layer2 = torch.nn.Linear(10, 10)

class Model(torch.nn.Module):
    def __init__(self):
        super().__init__()
        self.block1 = Block()
        self.block2 = Block()

model = Model()
torch.save(model.state_dict(), "model.pth")
```


## Show the contents in a model file

```sh
% ptmod "ls model.pth"
block1.layer1.weight
block1.layer1.bias
block1.layer2.weight
block1.layer2.bias
block2.layer1.weight
block2.layer1.bias
block2.layer2.weight
block2.layer2.bias
```

```sh
% ptmod "ls -l model.pth"
block1.layer1.weight: (10, 10)
block1.layer1.bias: (10,)
block1.layer2.weight: (10, 10)
block1.layer2.bias: (10,)
block2.layer1.weight: (10, 10)
block2.layer1.bias: (10,)
block2.layer2.weight: (10, 10)
block2.layer2.bias: (10,)
```

## Copy parameters

```sh
% rm -f out.pth
% ptmod "cp model.pth:block1 out.pth" "ls out.pth"
layer1.weight
layer1.bias
layer2.weight
layer2.bias
```

```sh
% rm -f out.pth
% ptmod "cp model.pth:block1 out.pth:foo" "ls out.pth"
foo.layer1.weight
foo.layer1.bias
foo.layer2.weight
foo.layer2.bias
```


## Remove parameters

```sh
% rm -f out.pth
% ptmod "cp model.pth out.pth" "rm out.pth:block1" "ls out.pth"
block2.layer1.weight
block2.layer1.bias
block2.layer2.weight
block2.layer2.bias
```

```sh
% rm -f out.pth
% ptmod "cp model.pth out.pth" "rm out.pth:block2.layer2" "ls out.pth"
block2.layer1.weight
block2.layer1.bias
block1.layer1.weight
block1.layer1.bias
block1.layer2.weight
block1.layer2.bias
```
