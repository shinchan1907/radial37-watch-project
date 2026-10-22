from cadgen import step, stl
from geometry import case_shape

@step(out='../STEP/case_study.step')
@stl(out='../STL/case_study.stl')
def case_study():
    return case_shape()

if __name__ == '__main__':
    case_study()
