#! python3
"""
Ease bookkeeping of dafny's measure-complexity runs 
by storing the log file with the args in the filename
"""

import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
# import subprocess as sp
import sys
import time
import logging
from datetime import datetime as dt, timedelta as td, timezone
import psutil
from quantiphy import Quantity
from typing import NoReturn
from sh import Command
from functools import partial
import webbrowser
#from darum import plot_distribution



def main():
    parser = argparse.ArgumentParser(description="Run dafny's measure-complexity, and store the log with additional context and bookeeping information.")
    parser.add_argument("dafnyfiles", nargs="+", help="The dafny file(s) to verify.")
    parser.add_argument("-e", "--extra_args", default="", help="A quoted string of extra arguments to pass to dafny")
    parser.add_argument("-d", "--dafnyexec", default="dafny", help="The dafny executable")
    parser.add_argument("-r", "--rseed", default=None, help="The random seed. By default is seeded with the current time.")
    parser.add_argument("-m", "--mut", default="10", help="Number of mutations. Default=%(default)s")
    parser.add_argument("-f", "--format", default="json", help=argparse.SUPPRESS) # CVS needs updating
    parser.add_argument("-s", "--filter-symbol", help="Only verify symbols containing this substring.")
    parser.add_argument("-l", "--limitRC", type=Quantity, default=Quantity("10M"), help="The Resource Count limit. Accepts magnitudes (K,M,G...). Default=%(default)s")
    parser.add_argument("-i", "--isolate-assertions",action="store_true")
    parser.add_argument("-c", "--verify-included-files",action="store_true", help="Verify included files")
    parser.add_argument("-z", "--z3-path", help="Dafny's ""solver-path"" argument")
    parser.add_argument("-o", "--output_dir", default="darum", help="Directory to store the results. Default=%(default)s")
    parser.add_argument("-v", "--verbose", action="count", default=0, help="Use multiple times to increase verbosity")
    parser.add_argument("--stop",action="store_true", help="Do not call plot_distribution after verification")

    args = parser.parse_args()

    logging.basicConfig() #level=numeric_level,format='%(levelname)s:%(message)s')
    logger = logging.getLogger(__name__)
    numeric_level = max(logging.DEBUG, logging.WARNING - args.verbose * 10)
    logger.setLevel(numeric_level)

    if args.verify_included_files:
        print("Using --verify-included-files. Beware, only the top file's source will be saved into the augmented log")

    try:
        os.makedirs(args.output_dir)
    except:
        pass
    IAstr = "_IA" if args.isolate_assertions else ""
    VIFstr = "_VIF" if args.verify_included_files else ""
    dafnyfiles_str = ""
    rseed = str(int(time.time())) if args.rseed is None else args.rseed
    source_dict  = {}
    for df in args.dafnyfiles:
        dfbase = os.path.basename(df)
        # with open(df, "rb") as f:
        #     digest = hashlib.file_digest(f, "md5")
        with open(df, "r") as f:
            src= f.read()
        mod_tstamp = os.stat(df).st_mtime
        mod_date = dt.fromtimestamp(mod_tstamp, tz=timezone.utc).isoformat()
        digest = hashlib.md5(bytes(src, encoding="utf-8"))
        hash = digest.hexdigest()
        dfsplit = os.path.splitext(dfbase)
        filenamehash = f"{dfsplit[0]}.H{hash[0:4]}{dfsplit[1]}"
        source_dict[dfbase] = {
            "contents": src,
            "hash": hash,
            "modified": mod_date, #to report changes it's more human-friendly to use the modif_date than a hash
        }
        dafnyfiles_str += f"_{dfsplit[0]}_H{hash[0:4]}"
        # take a snapshot of this input file, adding the same hash piece as in the log
        dfcopy = os.path.join(args.output_dir,filenamehash)
        if not os.path.exists(dfcopy):
            shutil.copy2(df,dfcopy)
    z3_str = f"_{Path(args.z3_path).name}" if args.z3_path else ""
    symbol_str = f"_s{args.filter_symbol}" if args.filter_symbol else ""
    dafnyexec_str= os.path.basename(args.dafnyexec) if args.dafnyexec != "dafny" else ""
    rseed_str = f"_r{args.rseed}" if args.rseed else ""
    extra_args_str = f"_E{args.extra_args}" if args.extra_args else ""
    argstring4filename = f"{dafnyexec_str}{dafnyfiles_str}_M{args.mut}_L{args.limitRC}{rseed_str}{IAstr}{VIFstr}{z3_str}{symbol_str}{extra_args_str}".replace("/","").replace("-","").replace(":","").replace(" ","")
    nowstr = dt.now().strftime('%m%d-%H%M%S')
    logfilename = os.path.join(args.output_dir, nowstr + argstring4filename)
    # for convenience, take another snapshot of each single-input-file with the same full filename as the log
    # if len(args.dafnyfiles)==1:
    #     df= args.dafnyfiles[0]
    #     dfsplit = os.path.splitext(df)
    #     shutil.copy2(df,logfilename+dfsplit[1])
    #log.debug(f"filename={filename}")
    #shell_line = fr"{args.dafnyexec} measure-complexity --log-format csv\;LogFileName='{filename}' {args.extra_args} {args.dafnyfile}"

    arglist = [
        # args.dafnyexec,
        "measure-complexity",
        "--random-seed", rseed,
        "--mutations", args.mut,
        "--log-format", f"{args.format};LogFileName={logfilename}.{args.format}",
        "--resource-limit", str(int(args.limitRC)),
        "--isolate-assertions" if args.isolate_assertions else "",
        "--verify-included-files" if args.verify_included_files else "",
        *(["--solver-path", args.z3_path] if args.z3_path else []),
        *(["--filter-symbol", args.filter_symbol] if args.filter_symbol else []),
        *args.extra_args.split(),
        *args.dafnyfiles
        ]
    logger.debug(f"Executing:{args.dafnyexec} {' '.join(arglist)}")
    # sys.stdout.flush()
    # sys.stderr.flush()
    # os.execvp(args.dafnyexec, arglist )

    #pitfalls: bufsize; blocking,

    import atexit
    def killProc():
        logger.debug("Killing the subprocess' group...")
        dafny_proc.kill_group()
    atexit.register(killProc)

    def process_output(stream, store, line):
        nonlocal mutation_tstamp
        nonlocal mutation_times
        nonlocal output_last_tstamp
        nonlocal counter_error
        nonlocal counter_success
        nonlocal state_error
        nonlocal delta_min_last
        now = dt.now()

        if "Starting verification of mutation" in line or "The total consumed resources are" in line:
            if mutation_tstamp is not None:
                delta = int((now - mutation_tstamp).total_seconds())
                if state_error:
                    counter_error +=1
                else:
                    counter_success += 1
                state_error = False
                l = f"DARUM: mutation took {delta} sec.\t{counter_success} successes, {counter_error} errors\n"
                print(l, end=None)
                store.append(l)
                mutation_times.append(delta)
            mutation_tstamp = now

        if "Error" in line:
            state_error = True
        prefix = f'{dt.now().strftime('%H:%M:%S')}: ' if args.verbose>2 else ""
        stream.write(prefix + line)
        store.append(line)
        output_last_tstamp = now
        delta_min_last = 0

    stdout_lines = []
    # stderr = []

    dafny = Command(args.dafnyexec)

    mutation_tstamp = None
    mutation_times = []
    output_last_tstamp = dt.now()
    counter_error = 0
    counter_success = 0
    state_error = False
    dafny_proc = dafny(arglist,_out=partial(process_output, sys.stdout, stdout_lines), _bg=True, _err_to_out=True, _ok_code=[0,1,2,3,4],_return_cmd=True, _new_session=True)
    # p = sp.Popen(arglist, bufsize=-1, stdout=sp.PIPE, stderr=sp.PIPE, text=True, process_group=0)
    # os.set_blocking(p.stdout.fileno(), False)
    # os.set_blocking(p.stderr.fileno(), False)
    pgid = dafny_proc.pgid 
    logger.debug(f"{pgid=}")

    procs_old = []
    delta_min_last = 0
    while dafny_proc.is_alive():
        procs = []
        for proc in psutil.process_iter(['pid', 'name']):
            try:
                proc_pgid = os.getpgid(proc.info['pid'])
                if pgid == proc_pgid:
                    procs.append(proc)
            except:
                pass
        if procs != procs_old:
            logger.info(f"""Child procs: {[f"{proc.info['pid']}({proc.info['name']})" for proc in procs]}""" )
            procs_old = procs
        delta = int((dt.now() - output_last_tstamp).total_seconds())
        if delta // 60 > delta_min_last:
            delta_min_last = delta // 60
            l = f"DARUM: no dafny output for {delta_min_last} minutes..."
            print(l)
            stdout_lines.append(l)
        time.sleep(1)

    dafny_proc.wait()
    atexit.unregister(killProc)

    exit_code = dafny_proc.exit_code
    logger.debug(f"{pgid=}, {exit_code=}")

    print()
    line = f"DARUM:{mutation_times=}"
    print(line)
    stdout_lines.append(line)
    # if a log file was created, add our own data to it
    if exit_code in [0,2,3,4]:
        with open(f"{logfilename}.{args.format}") as jsonfile:
            try:
                json_data = json.load(jsonfile)
                json_data["verificationResults"]
            except:
                logger.error("No verificationResults!")
        darum_context = {}
        darum_context['files']=source_dict
        darum_context['output']=stdout_lines
        darum_context['cmd']=[args.dafnyexec] + arglist
        json_data["darum"]=darum_context
        with open(f"{logfilename}.{args.format}",mode='w') as jsonfile:
            json.dump(json_data,jsonfile)
        print(f"DARUM:Generated augmented logfile at {logfilename}.{args.format}")

    print("\n-----------------------------------------------------------------------------------\n")

    # Check for leaked Z3 processes
    darum_context = dt.now()
    leaked_procs_old = []
    leaked_procs_found = False
    while True:
        elapsed = int((dt.now()-darum_context).total_seconds())
        leaked_procs = []
        for proc in psutil.process_iter(['pid', 'name']):
            try:
                proc_pgid = os.getpgid(proc.info['pid'])
                if pgid == proc_pgid:
                    leaked_procs.append(proc)
            except:
                pass
        if leaked_procs == []:
            break
        leaked_procs_found = True
        if leaked_procs != leaked_procs_old and elapsed>1:
            for proc in leaked_procs:
                logger.warning(f"Leaked process: {proc.info['name']} PID={proc.info['pid']}")
            leaked_procs_old = leaked_procs
        time.sleep(1)
    if leaked_procs_found and elapsed>1:
        logger.warning(f"Leaked processes finished after {elapsed} secs")

    if (args.stop):# or (exit_code not in [0,1,2,3,4]):
        return exit_code

    pd = Command("plot_distribution")
    pd_args = [
        f"{logfilename}.{args.format}",
        *([f"-{"v"*args.verbose}"] if args.verbose>0 else []),
        *(["--force-IA-mode"] if args.isolate_assertions else []),
        *(["--limitRC", str(args.limitRC)] if args.limitRC is not None else []),
    ]

    print(f"DARUM: continuing to `plot_distribution {' '.join(pd_args)}`")
    #print(pd(pd_args,_err_to_out=True))     #alternatives: _fg=True? or redirect _in=sys.stdin, ...
    pd(pd_args,_fg=True)

    return exit_code #from dafny, not from the plot!
