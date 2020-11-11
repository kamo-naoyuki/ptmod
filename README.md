# pytorch_model_operators
Command line utilies to modify serialized pytorch model states.

### Show the contents in a model file

```sh
% ptmop "ls model.pth"
>>>>>>>> model.pth
block1.layer1.weight
block1.layer2.weight
block1.layer2.bias
block2.layer1.weight
block2.layer2.weight
block2.layer2.bias
```

### Remove parameters

```sh
% cp model.pth out.pth
% ptmop "rm out.pth:block1" "ls out.pth"
>>>>>>>> model.pth
block2.layer1.weight
block2.layer2.weight
block2.layer2.bias
```

```sh
% cp model.pth out.pth
% ptmop "rm out.pth:block2.layer2" "ls out.pth"
>>>>>>>> model.pth
block1.layer1.weight
block1.layer2.weight
block1.layer2.bias
block2.layer1.weight
```

```sh
% ptmop "cp model.pth out.pth" "rm out.pth:block2.layer2" "ls out.pth"
>>>>>>>> model.pth
block1.layer1.weight
block1.layer2.weight
block1.layer2.bias
block2.layer1.weight
```

### Copy parameters

```sh
% ptmop "cp model.pth:block1 out.pth" "ls out.pth"
>>>>>>>> model.pth
layer1.weight
layer2.weight
layer2.bias
```

```sh
% ptmop "cp model.pth:block1 out.pth:foo" "ls out.pth"
>>>>>>>> model.pth
foo.layer1.weight
foo.layer2.weight
foo.layer2.bias
```
