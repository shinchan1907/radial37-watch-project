from cadgen import step, stl
from geometry import dial_shape

@step(out='../STEP/dial_study.step')
@stl(out='../STL/dial_study.stl')
def dial_study():
    return dial_shape()

if __name__ == '__main__':
    dial_study()
