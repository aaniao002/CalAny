# Coading Idea: Cal Anything

# solve problem
All currencies are exchangeable, eg:USD AUD TWD HDK ..., but is there any exchange path ( curr1 -> curr2 -> ... -> curr1 ) to get more money?  
`python3 ./calany.py` will resolve this.

# Backstory
define y=f(x) as one micro MetaCal, dozen of f will generate a way to do super complex calculation.

Abstract all data as MetaData( type + data ), if there's some cal path as follow:
```
b=f1(x)
c=f2(b)
d=f3(c)
y=f4(d)
```
then y=f4(f3(f2(f1(x))))

JUST a little more, if there's ton of f():
```
x->b
x->d
b->c
c->d
c->f
b->f
f->y
```
then we got y=f(x)
