# InterPenet
## Probabilistic evaluation of penetration of plate
#### Shinsuke Sakai   
 Emeritus Professor, The University of Tokyo, Japan   
 Visiting Professor, Yokohama National University, Japan

 ### Overview
For the risk evaluation of penetration caused by flying objects onto steel plates, the assessment of penetration probability is required. For the evaluation of penetration probability of flying objects on plates, Limit State Function Method (LSFM) is applied. Representative 11 penetration formulas are included. If you want to know the details of this package, refer to the following paper.

 S.Sakai and T. Kumagai,"Application of Limit State Function Method To Statistical Analysis of Ballistic Penetration", Proceedings of the 17th Hypervelocity Impatct Symbosium HVIS2024, Sept.9-13,2024,Tsukuba,Japan

### Installation
You can install the package via pip:
```python
pip install InterPenet
```

### Operation check
The following describes the method for checking when applying to penetration analysis using BRL formula. To execute this program, you need th input file 'BRL.pkl'. The 'BRL.pkl' is given in  the [site](https://github.com/ShinsukeSakai0321/InterPenet).


```python
from InterPenet import InterPenet as ip
bb=ip.Base()
bb.CalcPenet('BRL.pkl')
```

If the following output is obtained, it is working correctly.
```
Validation [['v_bl', 'satisfied'], ['Limp/d', 'satisfied'], ['b/d', 'satisfied'], ['Lsh/d', 'satisfied'], ['Su', 'not satisfied']]
*** Probabilistic analysis ***
[ BRL Formula ]
variable= ['b', 'd', 'm', 'v', 'Me']
beta= -0.5571767489022684
Alpha= [ 0.06413751  0.06413751 -0.0427838  -0.9006759   0.42275907]
Pf= 0.7112966629840962
*** Analysis of Balistic Limit Velocity ***
Vbl= 102.34312241793276
File= BRL.pkl
```
If you want to get the output as a dictionary, do it like this.
```python
from InterPenet import InterPenet as ip
bb=ip.Base()
dd=bb.CalcPenet2Df('BRL.pkl')
dd
```
The output will be displayed as follows.
```
{'Formula': 'BRL Formula',
 'Validation': [['v_bl', 'satisfied'],
  ['Limp/d', 'satisfied'],
  ['b/d', 'satisfied'],
  ['Lsh/d', 'satisfied'],
  ['Su', 'not satisfied']],
 'variable': ['b', 'd', 'm', 'v', 'Me'],
 'g_value': -7.422565340273962,
 'beta': -0.5571767489022684,
 'Alpha': array([ 0.06413751,  0.06413751, -0.0427838 , -0.9006759 ,  0.42275907]),
 'Pf': np.float64(0.7112966629840962),
 'Vbl': 102.34312241793276,
 'File': 'BRL.pkl'}
 ```







