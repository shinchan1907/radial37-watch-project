from cadgen import step, stl
from geometry import back_shape

@step(out='../STEP/caseback_study.step')
@stl(out='../STL/caseback_study.stl')
def caseback_study():
    return back_shape()

if __name__ == '__main__':
    caseback_study()
