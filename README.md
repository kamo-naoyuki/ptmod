# ptmod: Modify PyTorch model
Command line utilies to modify serialized pytorch model states.

## The definition of pytorch model file
In this tool, a model file should be the serialized `state_dict` object.

```python
# e.g.
import torch
class Model(torch.nn.Module):
    def __init__(self):
        self.linear1 = torch.nn.Linear(10, 10)
        self.linear2 = torch.nn.Linear(10, 10)

model = Model()
torch.save(model.state_dict(), "model.pth")
```


## Show the contents in a model file

```sh
% ptmod "ls model.pth"
block1.layer1.weight
block1.layer2.weight
block1.layer2.bias
block2.layer1.weight
block2.layer2.weight
block2.layer2.bias
```

## Copy parameters

```sh
% ptmod "cp model.pth:block1 out.pth" "ls out.pth"
layer1.weight
layer2.weight
layer2.bias
```

```sh
% ptmod "cp model.pth:block1 out.pth:foo" "ls out.pth"
foo.layer1.weight
foo.layer2.weight
foo.layer2.bias
```


## Remove parameters

```sh
% cp model.pth out.pth
% ptmop "rm out.pth:block1" "ls out.pth"
block2.layer1.weight
block2.layer2.weight
block2.layer2.bias
```

```sh
% cp model.pth out.pth
% ptmod "rm out.pth:block2.layer2" "ls out.pth"
block1.layer1.weight
block1.layer2.weight
block1.layer2.bias
block2.layer1.weight
```
