import warnings
import StringIO

import numpy as np
from numpy.testing import assert_array_equal

from pyne.endf import Library
from pyne.endf import convert as conv
from pyne.rxdata import DoubleSpinDict

import nose
from nose.tools import assert_equal

str_library = StringIO.StringIO(
""" $Rev:: 532      $  $Date:: 2011-12-05#$                             1 0  0    0
 1.002000+3 1.996800+0          1          0          0          0 128 1451    1
 0.000000+0 0.000000+0          0          0          0          6 128 1451    2
 1.000000+0 1.500000+8          1          0         10          7 128 1451    3
 0.000000+0 0.000000+0          0          0        211         17 128 1451    4
  1-H -  2 LANL       EVAL-FEB97 WEBDubois,Q.W.Alle,H.N.Casnowck   128 1451    5
 CH97,CH99            DIST-DEC06                       20111222    128 1451    6
----ENDF/B-VII.1      MATERIAL  128                                128 1451    7
-----INCIDENT NEUTRON DATA                                         128 1451    8
------ENDF-6 FORMAT                                                128 1451    9
                                                                   128 1451   10
 ****************************************************************  128 1451   11
                                                                   128 1451   12
 Lorem ipsum dolor sit amet, consectetur adipiscing elit.          128 1451   13
 Integer nec odio. Praesent libero. Sed cursus ante dapibus        128 1451   14
 diam. Sed nisi. Nulla quis sem at nibh elementum imperdiet.       128 1451   15
 Duis sagittis ipsum. Praesent mauris. Fusce nec tellus sed        128 1451   16
 augue semper porta.                                               128 1451   17
                                                                   128 1451   18
 ************************ C O N T E N T S ************************ 128 1451   19
                                1        451         27          0 128 1451   20
                                2        151         45          0 128 1451   21
                                3          1          1          0 128 1451   22
                                3          2          1          0 128 1451   23
                                3          3          1          0 128 1451   24
                                3         16          1          0 128 1451   25
                                3        102          1          0 128 1451   26
                                4          2          1          0 128 1451   27
 0.000000+0 0.000000+0          0          0          0          0 128 1  099999
 0.000000+0 0.000000+0          0          0          0          0 128 0  0    0
 1.876876+3 1.776576+0          0          0          1          0 128 2151    1
 5.513700+4 1.000000+0          0          0          4          0 128 2151    2
 2.700000+3 2.000000+5          1          1          1          2 128 2151    3
 0.000000+0 0.000000+0          0          0          4         10 128 2151    4
          2          3          5          2          7          1 128 2151    5
         10          6                                             128 2151    6
 0.500000+0 1.000000-1          0          0          2          0 128 2151    7
 1.000000+0 1.100000-1 2.000000+0          1         12          2 128 2151    8
 2.000000+5 1.000000+0 1.000000+1 2.000000+0 1.100000+0 3.100000+0 128 2151    9
 3.000000+6 2.000000+0 2.000000+1 3.000000+0 1.200000+0 3.200000+0 128 2151   10
 1.100000+0 1.110000-1 2.500000+0          1         12          2 128 2151   11
 3.100000+5 3.000000+0 1.100000+1 2.100000+0 2.100000+0 4.100000+0 128 2151   12
 4.100000+6 4.000000+0 2.100000+1 3.100000+0 2.200000+0 4.200000+0 128 2151   13
 2.300000+3 3.000000+5          1          1          0          1 128 2151   14
 5.000000-1 1.000000-1          0          0          1          0 128 2151   15
 1.000000+0 1.100000-1 1.000000+0          1         12          2 128 2151   16
 3.500000+5 1.000000+0 1.000000+1 2.000000+0 1.100000+0 3.100000+0 128 2151   17
 4.500000+6 2.000000+0 2.000000+1 3.000000+0 1.200000+0 3.200000+0 128 2151   18
 2.197178+3 1.781069+6          1          3          1          1 128 2151   19
 0.000000+0 0.000000+0          0          0          2          7 128 2151   20
          3          4          7          1                       128 2151   21
 2.500000+0 3.699209+3          1          0          1          0 128 2151   22
 2.399684-9 2.626370+5 2.000000+0          0          6          1 128 2151   23
 4.127773+3-3.956950-7 3.739684-5-3.872199+7 2.259559+5-3.096948-8 128 2151   24
 1.787886-1 1.634787+6          1          4          1          1 128 2151   25
 0.000000+0 0.000000+0          0          0          3         10 128 2151   26
          3          2          6          5         10          1 128 2151   27
 3.500000+0 2.145387-2          0          0          2          0 128 2151   28
 1.523605+6 0.000000+0          7          0         18          3 128 2151   29
 9.143204-3 1.601509+1-3.312654-7-3.460776+8-3.947879-5-1.646877-5 128 2151   30
 1.009363-5-1.861342-7-1.613360+7-7.549728+5-3.064120+9-2.961641+0 128 2151   31
-4.390193-5 2.303605+0-4.630212+5-3.237353+1-4.037885+4-3.231304+0 128 2151   32
 0.000000+0 0.000000+0 4.000000+0          0          2          0 128 2151   33
 1.000000+0 0.000000+0          0          0         24          2 128 2151   34
 1.029199+3-4.611259+5-4.348653+0 5.072331-8-2.722664+8 4.238546+4 128 2151   35
 2.881576+6-4.663196+5-4.754578-7-4.578510+1 1.040734+3 2.171429-7 128 2151   36
 4.485210+0-1.075272+3 5.228296-9 4.636330+4 9.996406-7-2.860366+4 128 2151   37
-2.751527+7 3.763842-8-3.333810-5-1.250613+0-4.636583-6 8.651338+1 128 2151   38
 2.000000+0 0.000000+0          0          0         12          1 128 2151   39
-1.703457-4 2.722273+9 2.950158-1 4.767819-1 4.506927-3 2.960170+3 128 2151   40
-4.006882+8-2.188708-4 3.262820+4 2.372937+6 4.251123-6 4.998481-6 128 2151   41
 0.000000+0 0.000000+0 5.000000+0          0          1          0 128 2151   42
 3.000000+0 0.000000+0          0          0         12          1 128 2151   43
-3.211014+1-2.011165+3 4.178337+5 1.640997+2 1.122313-5 1.537114-2 128 2151   44
 4.634918-8-3.884155-4 2.384144-9-3.745465-7-1.646941-2-2.894650-8 128 2151   45
 0.000000+0 0.000000+0          0          0          0          0 128 2  099999
 0.000000+0 0.000000+0          0          0          0          0 128 0  0    0
 1.989875+3 1.998644+0          0          0          0          0 128 3  1    1
 0.000000+0 0.000000+0          0          0          0          0 128 3  099999
 1.012000+3 1.231241+0          0          0          0          0 128 3  2    1
 0.000000+0 0.000000+0          0          0          0          0 128 3  099999
 1.123123+3 1.123113+0          0          0          0          0 128 3  3    1
 0.000000+0 0.000000+0          0          0          0          0 128 3  099999
 7.984533+3 1.125535+0          1          0          0          0 128 3 16    1
 0.000000+0 0.000000+0          0          0          0          0 128 3  099999
 1.948720+3 1.145243+0          0          0          0          0 128 3102    1
 0.000000+0 0.000000+0          0          0          0          0 128 3  099999
 0.000000+0 0.000000+0          0          0          0          0 128 0  0    0
 1.983232+3 1.934732+0          0          2          0          0 128 4  2    1
 0.000000+0 0.000000+0          0          0          0          0 128 4  099999
 0.000000+0 0.000000+0          0          0          0          0 128 0  0    0
 0.000000+0 0.000000+0          0          0          0          0   0 0  0    0
 0.000000+0 0.000000+0          0          0          0          0  -1 0  0    0
 $Rev:: 512      $  $Date:: 2006-12-05#$                             1 0  0    0
 1.003100+3 2.098312+0          1          0          0          1 131 1451    1
 0.564324+0 1.123121+0          0          0          0          6 131 1451    2
 1.905018+0 2.401998+7          1          0         10          7 131 1451    3
 0.109590+0 0.123112+0          0          0         90          8 131 1451    4
  1-H -  3 LANL       EVAL-NOV01 W.P.Pike                          131 1451    5
PRC  42, 438 (1990)   DIST-DEC06                       20111222    131 1451    6
----ENDF/B-VII.1      MATERIAL  131                                131 1451    7
-----INCIDENT NEUTRON DATA                                         131 1451    8
------ENDF-6 FORMAT                                                131 1451    9
                                                                   131 1451   10
*** Mauris massa. Vestibulum lacinia arcu eget nulla. Class *****  131 1451   11
aptent taciti sociosqu ad litora torquent per conubia nostra, per  131 1451   12
inceptos himenaeos. Curabitur sodales ligula in libero. Sed        131 1451   13
*****************************************************************  131 1451   14
                                                                   131 1451   15
                                1        451         21          1 131 1451   16
                                2        151         22          1 131 1451   17
                                3          1          1          1 131 1451   18
                                3          2          1          1 131 1451   19
                                3         16          1          1 131 1451   20
                                4          2          1          1 131 1451   21
 0.000000+0 0.000000+0          0          0          0          0 131 1  099999
 0.000000+0 0.000000+0          0          0          0          0 131 0  0    0
 1.212311+3 2.898897+0          0          0          1          0 131 2151    1
 5.513700+4 1.000000+0          0          0          2          0 131 2151    2
 1.700000+3 1.000000+5          2          1          0          0 131 2151    3
 3.500000+0 5.101200-1          0          0          2          0 131 2151    4
 1.357310+2 0.000000+0          0          0         18          3 131 2151    5
 1.800000+3          6 1.000000+0 2.078520-1 1.000000-2 0.000000+0 131 2151    6
 2.100000+3          7 2.000000+0 6.088000-1 2.000000-2 0.000000+0 131 2151    7
 3.100000+3          8 3.000000+0 3.120000-1 3.000000-2 0.000000+0 131 2151    8
 1.357310+2 0.000000+0          1          0         18          3 131 2151    9
 1.810000+3          9 4.000000+0 4.489400-1 8.000000-2 0.000000+0 131 2151   10
 2.110000+3         10 5.000000+0 8.497500-1 7.000000-2 0.000000+0 131 2151   11
 3.110000+3         11 6.000000+0 9.524900-1 6.000000-2 0.000000+0 131 2151   12
 1.100000+5 2.000000+7          2          1          0          0 131 2151   13
 2.000000+0 5.101200-1          0          0          2          0 131 2151   14
 1.357310+2 0.000000+0          2          0         18          3 131 2151   15
 1.801000+3          0 1.100000+0 3.078520-1 1.000000-2 0.000000+0 131 2151   16
 2.101000+3          1 2.100000+0 7.088000-1 2.000000-2 0.000000+0 131 2151   17
 3.101000+3          2 3.100000+0 2.120000-1 3.000000-2 0.000000+0 131 2151   18
 1.357310+2 0.000000+0          1          0         18          3 131 2151   19
 1.812000+3          3 4.100000+0 5.489400-1 8.000000-2 0.000000+0 131 2151   20
 2.112000+3          4 5.100000+0 9.497500-1 7.000000-2 0.000000+0 131 2151   21
 3.112000+3          5 6.100000+0 0.524900-1 6.000000-2 0.000000+0 131 2151   22
 0.000000+0 0.000000+0          0          0          0          0 131 2  099999
 0.000000+0 0.000000+0          0          0          0          0 131 0  0    0
 1.304918+3 2.582082+0          0          0          0          0 131 3  1    1
 0.000000+0 0.000000+0          0          0          0          0 131 3  099999
 1.001200+3 2.912396+0          0          0          0          0 131 3  2    1
 0.000000+0 0.000000+0          0          0          0          0 131 3  099999
 1.001900+3 2.988596+0          0          0          0          0 131 3 16    1
 0.000000+0 0.000000+0          0          0          0          0 131 3  099999
 0.000000+0 0.000000+0          0          0          0          0 131 0  0    0
 1.001900+3 2.989116+0          0          1          0          0 131 4  2    1
 0.000000+0 0.000000+0          0          0          0          0 131 4  099999
 0.000000+0 0.000000+0          0          0          0          0 131 0  0    0
 0.000000+0 0.000000+0          0          0          0          0   0 0  0    0
 0.000000+0 0.000000+0          0          0          0          0  -1 0  0    0
 $Rev:: 512      $  $Date:: 2006-12-05#$                             1 0  0    0
 4.019200+3 6.192500+0          1          0          0          1 419 1451    1
 0.123000+0 0.063200+0          0          0          0          6 419 1451    2
 1.000230+0 8.100130+6          1          0         10          7 419 1451    3
 0.001200+0 0.001600+0          0          0         47         10 419 1451    4
  4-Be-  7 LANL       EVAL-JUN04 E.N.Trix                          419 1451    5
                      DIST-DEC06                       20111222    419 1451    6
----ENDF/B-VII.1      MATERIAL  419                                419 1451    7
-----INCIDENT NEUTRON DATA                                         419 1451    8
------ENDF-6 FORMAT                                                419 1451    9
                                                                   419 1451   10
 ***************************************************************** 419 1451   11
dignissim lacinia nunc. Curabitur tortor. Pellentesque nibh.       419 1451   12
Aenean quam. In scelerisque sem at dolor. Maecenas mattis. Sed     419 1451   13
convallis tristique sem.                                           419 1451   14
 ***************************************************************** 419 1451   15
                                1        451         22          1 419 1451   16
                                2        151         53          1 419 1451   17
                                3          2          5          1 419 1451   18
                                3        600          4          1 419 1451   19
                                3        650          1          1 419 1451   20
                                3        800          1          1 419 1451   21
                                4          2          2          1 419 1451   22
 0.000000+0 0.000000+0          0          0          0          0 419 1  099999
 0.000000+0 0.000000+0          0          0          0          0 419 0  0    0
 1.520000+2 4.400259+9          0          0          2          0 419 2151    1
 2.152212-9 2.776505-3          0          1          1          0 419 2151    2
 3.724629+1 3.538532+6          2          1          1          1 419 2151    3
 0.000000+0 0.000000+0          0          0          2         10 419 2151    4
          2          3          10         6                       419 2151    5
 1.500000+0 1.865419+9          0          0          5          1 419 2151    6
-2.625837-2-1.457011+4-3.267593-4 3.959905+3-3.440459-2            419 2151    7
-1.263108-1 0.000000+0 4.000000+0          0          1          0 419 2151    8
 0.000000+0 0.000000+0 4.000000+0          3         11          0 419 2151    9
-3.276558-9 3.000000+0 1.499031-3-4.455678-9 2.910100-5 0.000000+0 419 2151   10
-4.284304+2-3.856415-8 9.065534-7-3.355711+6-1.847975+6            419 2151   11
 4.242961+4-4.242156+9          0          1          3          0 419 2151   12
-4.315613-5 2.891921+6          2          1          0          0 419 2151   13
 4.500000+0 3.751025-7          1          0          6          2 419 2151   14
-4.130223+6-3.793486+5 3.513877+2-6.072241-9-1.787864+3-1.162246+3 419 2151   15
-7.832899-5 0.000000+0 2.000000+0          0          2          0 419 2151   16
 0.000000+0 0.000000+0 2.000000+0          2         12          0 419 2151   17
 3.636791-1 3.000000+0 4.476397+9 8.789695+2 1.833746-9 0.000000+0 419 2151   18
-2.210171-1-2.561209+6 3.534863-9 4.970383+3-4.524614+0-3.986952-3 419 2151   19
 0.000000+0 0.000000+0 2.000000+0          1         12          0 419 2151   20
 1.979410-6-4.000000+0-4.264745-1 3.042416+0-4.427212+7 0.000000+0 419 2151   21
 2.163723-2 2.421080+5-9.370260+7-2.706321-7-3.037705+0 1.889285+1 419 2151   22
 4.648092-4 0.000000+0 3.000000+0          0          1          0 419 2151   23
 0.000000+0 0.000000+0 3.000000+0          3         12          0 419 2151   24
 2.804009-5 4.000000+0 3.181707+3 3.885315-9-3.382438+3 0.000000+0 419 2151   25
 2.376630+2 7.198625-2-5.887887-8-4.380016-5 1.747888-6-4.104291-9 419 2151   26
-3.639532-6-1.965467+3          2          1          0          0 419 2151   27
 3.500000+0 4.391826-7          1          0          7          1 419 2151   28
-2.723837-2-8.755303-2 2.245337-2-9.034520+2 2.252098+5 2.666587+2 419 2151   29
 3.747872-3                                                        419 2151   30
-2.368259-8 0.000000+0 4.000000+0          0          1          0 419 2151   31
 0.000000+0 0.000000+0 4.000000+0          4         13          0 419 2151   32
-9.824193-5 5.000000+0 4.676826-4-4.336597+0-9.045122+2 0.000000+0 419 2151   33
 3.699655-9-3.919000+5 8.467144-3-3.737007+9-5.750577+7-9.588021+8 419 2151   34
-3.280571+7                                                        419 2151   35
 1.754489+2 1.593056+1          2          2          0          0 419 2151   36
 5.000000-1 4.145900-5          1          0          2          0 419 2151   37
-1.187125-7 0.000000+0 5.000000+0          0          2          0 419 2151   38
 6.000000+0 0.000000+0          3          0         12          1 419 2151   39
 0.000000+0 0.000000+0 4.003466-3-2.709252-8 0.000000+0 5.075078+7 419 2151   40
 6.469007-9-2.062519+7-7.116815-5 1.562553-4 2.341246-9 4.397092+0 419 2151   41
 7.000000+0 0.000000+0          3          0         12          1 419 2151   42
 0.000000+0 0.000000+0 3.215655-1 2.913648-8 0.000000+0-4.040338+3 419 2151   43
-6.162365+2 4.264049+5 2.088009+8 2.756941+1 6.978406-1-1.334121-9 419 2151   44
-5.702860+9 0.000000+0 6.000000+0          0          2          0 419 2151   45
 8.000000+0 0.000000+0          2          0         18          2 419 2151   46
 0.000000+0 0.000000+0 6.019205-4 4.315267+8 0.000000+0 4.241206+5 419 2151   47
 4.199534+1 1.769801-1 1.378667-8 9.070620+2-4.490878-9 2.721648+1 419 2151   48
 4.859555+8-2.330988-6-1.872580+5-2.816019-1-2.982221+6-1.048786+1 419 2151   49
 9.000000+0 0.000000+0          2          0         18          2 419 2151   50
 0.000000+0 0.000000+0-4.253833-1-2.269388+0 0.000000+0 4.732644-4 419 2151   51
-5.873521-3-4.808214+9 5.089619+5 4.836683+0 2.772702-3-4.865151-8 419 2151   52
-2.659480-9 1.044275+8-1.393749+2-4.189996-6-9.596467-4 3.942829+9 419 2151   53
 0.000000+0 0.000000+0          0          0          0          0 419 2  099999
 0.000000+0 0.000000+0          0          0          0          0 419 0  0    0
 4.284918+3 6.292347+0          0          0          0          0 419 3  2    1
 4.047593+5-4.245658-8          0-4.651348+3          7         20 419 3  2    2
          6          4          9          2         12          1 419 3  2    3
         13          5         15          3         17          4 419 3  2    4
         20          1                                             419 3  2    5
 0.000000+0 0.000000+0          0          0          0          0 419 3  099999
 4.193742+3 6.287192+0          0          0          0          0 419 3600    1
 3.863437-5-7.373532-7          0 8.675483-1          6         27 419 3600    2
          2          6          8          5          9          4 419 3600    3
         11          3         13          2         27          1 419 3600    4
 0.000000+0 0.000000+0          0          0          0          0 419 3  099999
 4.192847+3 6.874398+0          0          0          0          0 419 3650    1
 0.000000+0 0.000000+0          0          0          0          0 419 3  099999
 4.897498+3 6.287322+0          0          0          0          0 419 3800    1
 0.000000+0 0.000000+0          0          0          0          0 419 3  099999
 0.000000+0 0.000000+0          0          0          0          0 419 0  0    0
 4.898421+3 6.768123+0          0          1          0          0 419 4  2    1
 2.123124+6 8.123142-6 2.123212+6 8.231231-6-2.231211+6 8.123421-6 419 4  2    2
 0.000000+0 0.000000+0          0          0          0          0 419 4  099999
 0.000000+0 0.000000+0          0          0          0          0 419 0  0    0
 0.000000+0 0.000000+0          0          0          0          0   0 0  0    0
 0.000000+0 0.000000+0          0          0          0          0  -1 0  0    0
""")


library = Library(str_library)
library._read_mf2(128)
library._read_mf2(131)
library._read_mf2(419)

def array_from_ENDF(fh):
    return np.genfromtxt(fh,
                         delimiter=11,
                         converters={0: conv, 1: conv, 2: conv,
                                     3: conv, 4: conv, 5: conv})

def test_mats():
    for mat_id in library.mats:
        assert_in(mat_id, [128, 131, 419])


def test_get():
    obs = library.get(419, 4, 2)

    exp = np.array([4.898421e+3, 6.768123e+0, 0,
                    1, 0, 0, 2.123124e+6, 8.123142e-6,
                    2.123212e+6, 8.231231e-6,
                    -2.231211e+6, 8.123421e-6])
    badkey = library.get(111, 1, 1)
    assert_array_equal(exp, obs)
    assert_equal(badkey, False)


def test_unresolved_resonances_a():
    # Case A (ENDF Manual p.70)

    obs = library.mat131['data']['unresolved']

    exp_string = StringIO.StringIO(
        """ 1.801000+3          0 1.100000+0 3.078520-1 1.000000-2 0.000000+0
2.101000+3          1 2.100000+0 7.088000-1 2.000000-2 0.000000+0
3.101000+3          2 3.100000+0 2.120000-1 3.000000-2 0.000000+0""")
    exp_LIST = dict(zip(('D','AJ','AMUN','GN0','GG'),
                        array_from_ENDF(exp_string).transpose()))
    obs_LIST = obs[1][2][2,2]

    for key in exp_LIST:
        assert_array_equal(exp_LIST[key], obs_LIST[key])
    pass

def test_unresolved_resonances_b():
    # Case B (ENDF Manual p. 70)
    obs = library.mat419['data']['unresolved']
    # For the spin=4.5, L=3, J=4 section in the first isotope
    obs_1 = obs[0][2][4.5,3,4]
    exp_string_1 = StringIO.StringIO(
        """ 0.000000+0 0.000000+0 3.000000+0          3         12          0
 2.804009-5 4.000000+0 3.181707+3 3.885315-9-3.382438+3 0.000000+0
 2.376630+2 7.198625-2-5.887887-8-4.380016-5 1.747888-6-4.104291-9
""")
    exp_array_1 = array_from_ENDF(exp_string_1)
    exp_1 = dict(zip((0,0,'L','MUF','NE+6',0),exp_array_1[0]))
    exp_1.update(dict(zip(('D','AJ','AMUN','GN0','GG'),exp_array_1[1])))
    exp_1.update({'GF':exp_array_1[2]})
    exp_1['AWRI'] = np.array((4.648092e-4))
    del exp_1[0]
    for key in exp_1:
        assert_array_equal(obs_1[key], exp_1[key])
    # For the spin=3.5, L=4, J=5 section in the second isotope
    obs_2 = obs[1][2][3.5,4,5]
    exp_string_2 = StringIO.StringIO(
        """ 0.000000+0 0.000000+0 4.000000+0          4         13          0
-9.824193-5 5.000000+0 4.676826-4-4.336597+0-9.045122+2 0.000000+0
 3.699655-9-3.919000+5 8.467144-3-3.737007+9-5.750577+7-9.588021+8
-3.280571+7                                                       
""")
    exp_array_2 = array_from_ENDF(exp_string_2)
    exp_2 = dict(zip((0,0,'L','MUF','NE+6',0),exp_array_2[0]))
    exp_2.update(dict(zip(('D','AJ','AMUN','GN0','GG'),exp_array_2[1])))
    exp_2.update({'GF':exp_array_2[2:].flat[:exp_2['NE+6']-6]})
    exp_2['AWRI'] = np.array((-2.368259e-8))
    del exp_2[0]
    for key in exp_2:
        assert_array_equal(obs_2[key], exp_2[key])

    # for the ES
    obs_ES = obs[1][2]['ES']
    exp_ES_string = StringIO.StringIO(
        """-2.723837-2-8.755303-2 2.245337-2-9.034520+2 2.252098+5 2.666587+2
 3.747872-3                                                       
""")
    exp_ES = array_from_ENDF(exp_ES_string).flat[:7]
    assert_array_equal(obs_ES, exp_ES)


def test_unresolved_resonances_c():
    # Case C (ENDF Manual p. 70)
    exp_str = StringIO.StringIO(
        """ 9.000000+0 0.000000+0          2          0         18          2
 0.000000+0 0.000000+0-4.253833-1-2.269388+0 0.000000+0 4.732644-4
-5.873521-3-4.808214+9 5.089619+5 4.836683+0 2.772702-3-4.865151-8
-2.659480-9 1.044275+8-1.393749+2-4.189996-6-9.596467-4 3.942829+9
""")
    obs = library.mat419['data']['unresolved'][3][2][0.5,6,9]
    exp_array = array_from_ENDF(exp_str)
    exp = dict(zip(('ES','D','GX','GN0','GG','GF'),
                   exp_array[2:].transpose()))
    exp.update(dict(zip(('AJ',0,'INT',0,'6*NE+6','NE',0,0,'AMUX','AMUN','AMUG',
                         'AMUF'),
                        exp_array[:2].flat)))
    exp['AWRI'] = -5.702860e+9
    for key in obs:
        assert_array_equal(obs[key], exp[key])


def test_DoubleSpinDict():
    subject = DoubleSpinDict({(3.499999999998, 2, 1):{'A':'a', 'B':'b'},
                              (2.000000000012, 3, 4):{'C':'c', 'D':'d'}})
    subject.update({(3.500000000011,8,9):{'E':'e', 'F':'f'}})

    obs = subject[(3.48, 8, 9)]
    exp = {'E':'e', 'F':'f'}
    assert_equal(exp, obs)

def test_resolved_breitwigner():
 # The section looks like this:
 #         EL         EH        LRU        LRF        NRO       NAPS 419 2151    3
 # 0.000000+0 0.000000+0          0          0         NR         NP 419 2151    4
 #        SPI         AP          0          0        NLS          0 419 2151    5
 #       AWRI         QX          L        LRX      6*NRS        NRS 419 2151    6
 #         ER         AJ         GT         GN         GG         GF 419 2151    7
 #         ER         AJ         GT         GN         GG         GF 419 2151    8
 #       AWRI         QX          L        LRX      6*NRS        NRS 419 2151    6
 #         ER         AJ         GT         GN         GG         GF 419 2151    7
 #         ER         AJ         GT         GN         GG         GF 419 2151    8

    data = library.mat128['data']['resolved']
    # Check to see if NRO is reading from the right place.
    # NRO = 0 case
    assert_equal(data[-2][-1]['NRO'], 0)
    # NRO = 1 case
    # Check to see if NAPS is reading from the right place
    assert_equal(data[-2][-1]['NAPS'], 1)
    # Check to see if SPI, NLS are reading from the right place
    assert_equal(data[-2][-1]['SPI'], 0.5)
    assert_equal(data[-2][-1]['NLS'], 1)
    # Check to see if the data is alright...
    expected = {'ER': np.array([350000.0, 4500000.0]),
                'AJ': np.array([1.0, 2.0]),
                'GT': np.array([10., 20.]),
                'GN': np.array([2., 3.]),
                'GG': np.array([1.1, 1.2]),
                'GF': np.array([3.1,3.2])}
    for key in data[-2][2][0.5,1]:
        assert_array_equal(data[-2][2][0.5,1][key],expected[key])

def test_resolved_reichmoore():
# The section looks like this:
#         EL         EH        LRU        LRF        NRO       NAPS 419 2151    3
# 0.000000+0 0.000000+0          0          0         NR         NP 419 2151    4
#        SPI         AP        LAD          0        NLS       NLSC 419 2151    5
#       AWRI        APL          L          0      6*NRS        NRS 419 2151    6
#         ER         AJ         GN         GG        GFA        GFB 419 2151    7

    subsection = library.structure[128]['data']['resolved'][1]
    print subsection[2][2.5,2]
    assert_array_equal(subsection[2]['int']['E'], np.array([3,7]))
    assert_array_equal(subsection[2]['int']['AP(E)'], np.array([4,1]))
    obs_data = subsection[2][2.5,2]
    exp_data = {'ER': np.array(4.127773e+3),
                'AJ': np.array(-3.956950e-7),
                'GN': np.array(3.739684e-5),
                'GG': np.array(-3.872199e+7),
                'GFA': np.array(2.259559e+5),
                'GFB': np.array(-3.096948e-8)}
    for key in subsection[2][2.5,2]:
        assert_array_equal(obs_data[key], exp_data[key])

def test_resolved_adleradler():
# The section looks like this:
# [MAT, 2,151/ 0.0, 0.0, 0, 0, NR, NP/ Eint / AP(E)] TAB1
# [MAT, 2,151/ SPI, AP,0,0,NLS,0] CONT
# [MAT, 2,151/ AWRI, 0.0, LI,0, 6*NX, NX
# AT1 , AT2 , AT3 , AT4 , BT1 , BT2 ,
# AF1 , --------------------, BF2 ,
# AC1 , --------------------, BC2 ] LIST
# [MAT, 2,151/ 0.0, 0.0,L,0,NJS,0] CONT(l)
# [MAT, 2,151/ AJ, 0.0,0,0,12*NLJ, NLJ/
# DET1 , DWT1 , GRT1 , GIT1 , DEF1 , DWF1 ,
# GRF1 , GIF1 , DEC1 , DWC1 , GRC1 , GIC1 ,
# DET2 , DWT2 , GIC2 , --------------
# DET3 ,---------------------------
# --------------------------------
# ------------------------, GICN LJ ] LIST
    subsection = library.structure[128]['data']['resolved'][0]
    # Test to see if the LIST records read in right
    exp_LIST = {'DET': -3.211014e+1, 'DWT': -2.011165e+3,'GRT': 4.178337e+5,
                'GIT': 1.640997e+2, 'DEF': 1.122313e-5, 'DWF': 1.537114e-2,
                'GRF': 4.634918e-8, 'GIF': -3.884155e-4, 'DEC': 2.384144e-9,
                'DWC': -3.745465e-7, 'GRC': -1.646941e-2, 'GIC': -2.894650e-8}

    obs_LIST = subsection[2][3.5,5,3]

    for key in exp_LIST:
        assert_array_equal(exp_LIST[key],obs_LIST[key])

    exp_bg_string = StringIO.StringIO(
        """ 9.143204-3 1.601509+1-3.312654-7-3.460776+8-3.947879-5-1.646877-5
 1.009363-5-1.861342-7-1.613360+7-7.549728+5-3.064120+9-2.961641+0
-4.390193-5 2.303605+0-4.630212+5-3.237353+1-4.037885+4-3.231304+0""")
    exp_bg = dict(zip(('A1','A2','A3','A4','B1','B2'),
                      array_from_ENDF(exp_bg_string).transpose()))

    obs_bg = subsection[2]['bg']
    print subsection[0]
    for key in exp_bg:
        assert_array_equal(exp_bg[key],obs_bg[key])

def test_resolved_rmatrix():
    pass

def test_xs():
    # Read in the data
    library._read_xs(419, 600)
    library._read_xs(419, 2)

    # Manually find where the data should be reading from and check if it is
    # consistent with what the program is doing.
    exp_2_str = StringIO.StringIO(
        """ 4.284918+3 6.292347+0          0          0          0          0
 4.047593+5-4.245658-8          0-4.651348+3          7         20
          6          4          9          2         12          1
         13          5         15          3         17          4
         20          1                                            """)
    exp_2_a = array_from_ENDF(exp_2_str)
    exp_2 = dict(zip(('Eint', 'sigma(E)'),
                     (exp_2_a[2:].flat[:14:2], exp_2_a[2:].flat[1:14:2])))
    obs_2 = library.mat419['data']['xs'][0][1]

    exp_600_str = StringIO.StringIO(
        """ 4.193742+3 6.287192+0          0          0          0          0
 3.863437-5-7.373532-7          0 8.675483-1          6         27
          2          6          8          5          9          4
         11          3         13          2         27          1""")

    exp_600_a = array_from_ENDF(exp_600_str)
    exp_600 = dict(zip(('Eint', 'sigma(E)'),
                     (exp_600_a[2:].flat[::2], exp_600_a[2:].flat[1::2])))
    obs_600 = library.mat419['data']['xs'][1][1]

    for key in obs_2:
        assert_array_equal(obs_2[key], exp_2[key])
        assert_array_equal(obs_600[key], exp_600[key])

    # Heck, why not check the flags too?
    obs_600_flags = library.mat419['data']['xs'][1][2]
    exp_600_flags = dict(zip(('QM','QI',0,'LM','NR','NP'),
        exp_600_a[1]))#
    exp_600_flags.update({'ZA': 4.193742e+3, 'AWR': 6.287192})
    del exp_600_flags[0]
    assert_equal(obs_600_flags, exp_600_flags)


def test_U235():
    """This test file can be found here:
    http://t2.lanl.gov/data/data/ENDFB-VII.1-neutron/U/235
    It is very big (51 MB), so it is not included."""
    # u235 = Library('U235.txt')
    # print u235.mat9228['data']['unresolved'][0]
    pass

if __name__ == "__main__":
    nose.main()
