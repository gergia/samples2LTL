import sys
from rq import get_current_job

from flie.utils.Traces import ExperimentTraces
from flie.solverRuns import run_solver
import json


import traceback


# Just for testing


def learn_formula(task):
    # This creates a Task instance to save the job instance and job result

    # Get job
    job = get_current_job()

    task.status = "working"
    task.save()

    # Perform task
    # time.sleep (1)
    try:
        # Compute result

        traces = ExperimentTraces()
        print("received data: {}".format(task.data))
        data = json.loads(task.data)
        print("received data json: {}".format(data))
        traces.readTracesFromFlieJson(data)



        try:
            numberOfFormulas = data['number-of-formulas']
        except:
            numberOfFormulas = 1

        try:
            maxDepth = data['max-depth-of-formula']
        except:
            maxDepth = 5

        print(traces)
        [formulas, timePassed] = run_solver(finalDepth = maxDepth, traces = traces, maxNumOfFormulas = numberOfFormulas, startValue=1, step=1)

        # Save task and mark it finished
        task.result = [f.prettyPrint(top=True) for f in formulas]
        task.status = 'finished'
        task.save()
    except Exception:

        task.result = "sth went wrong"
        traceback.print_exc(file = sys.stdout)
        task.status = 'error'
        task.save()

    return