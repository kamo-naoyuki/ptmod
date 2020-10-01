# pytorch_model_operators
Command line utilies to modify the serialized pytorch model states.

### ptmop_ls

```sh
ptmop_ls model.pth
ptmop_ls model.pth "a/d"
```

### ptmop

```sh
ptmop model.pth modified.pth "mv a/b a/d; cp a/d a/e; rm a/d"
```

- All operations work recursively for dict type values
- With `-f` option, the existing values can be overwritten.


```sh
ptmop model.pth modified.pth "mv -f a/b a/c; cp -f a/d a/b"
```

`ptmop` command also has `ls` command.

```sh
ptmop model.pth /dev/null "ls"  # modified.pth is same as model.pth
```

### ptmop_average, ptmop_sum

```sh
ptmop_average -O out.pth model1.pth model2.pth [model3.pth ...]
ptmop_sum -O out.pth model1.pth model2.pth [model3.pth ...]
```

- ERROR if each model has one or more different keys.
- Int values are summed instead averaging in `ptmop_average` 

### ptmop_merge

Merge multiple models having difference keys into one

```sh
ptmop_merge -O out.pth model1.pth model2.pth [model3.pth ...]
ptmop_merge -f -O out.pth model1.pth model2.pth [model3.pth ...]
```

- ERROR if each model has one or more same keys.
- With `-f` option, the value of former model is used if same keys are found.

### ptmop_extract

```sh
ptmop_extract model.pth out.npy "a/b"                # Extract a value as a numpy file
ptmop_extract model.pth out.npz "a"                  # Extract a dict as a npz file
ptmop_extract --format pickle model.pth out.npz "a"  # Save using pickle.dump
ptmop_extract --format torch model.pth out.npz "a"   # Save using torch.save
```
