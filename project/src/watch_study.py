from cadgen import step, build123d as bd
from case_study import case_study
from dial_study import dial_study
from caseback_study import caseback_study

@step(out='../STEP/watch_study.step')
def watch_study():
    return bd.Compound(children=[case_study(), dial_study(), caseback_study()])

if __name__ == '__main__':
    watch_study()
