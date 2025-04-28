import os
import pytest
import shutil
import asyncio
import sys
from dv_flow.mgr import TaskListenerLog, TaskSetRunner, TaskSpec, ExtRgy, PackageLoader
from dv_flow.mgr.task_graph_builder import TaskGraphBuilder
from dv_flow.mgr.util import loadProjPkgDef
import dv_flow.libhdlsim as libhdlsim

sims = None

def get_available_sims():
    global sims

    sims = []
    for sim_exe,sim in {
        "iverilog": "ivl",
        "verilator": "vlt",
        "vcs": "vcs",
        "vsim": "mti",
        "xsim": "xsm",
    }.items():
        if shutil.which(sim_exe) is not None:
            sims.append(sim)
    return sims

@pytest.mark.parametrize("sim", get_available_sims())
def test_simple(tmpdir, request,sim):
    data_dir = os.path.join(os.path.dirname(__file__), "data")
    runner = TaskSetRunner(os.path.join(tmpdir, 'rundir'))

    def marker_listener(marker):
        raise Exception("marker")

    builder = TaskGraphBuilder(
        PackageLoader(marker_listeners=[marker_listener]).load_rgy(['std', 'hdlsim.%s' % sim]),
        os.path.join(tmpdir, 'rundir'))

    top_v = builder.mkTaskNode(
        'std.FileSet',
        name="top_v",
        type="systemVerilogSource",
        base=data_dir,
        include="*.v",
        needs=[])
    
    sim_img = builder.mkTaskNode(
        "hdlsim.%s.SimImage" % sim,
        name="sim_img",
        top=['top'],
        needs=[top_v])

    sim_run = builder.mkTaskNode(
        "hdlsim.%s.SimRun" % sim,
        name="sim_run",
        needs=[sim_img])

    runner.add_listener(TaskListenerLog().event)
    out = asyncio.run(runner.run(sim_run))

    assert runner.status == 0

    #print("out: %s" % str(out))

    rundir_fs = None
    for fs in out.output:
        if fs.type == 'std.FileSet' and fs.filetype == "simRunDir":
            rundir_fs = fs

    assert rundir_fs is not None
    assert rundir_fs.src == "sim_run"

    assert os.path.isfile(os.path.join(rundir_fs.basedir, "sim.log"))
    with open(os.path.join(rundir_fs.basedir, "sim.log"), "r") as f:
        sim_log = f.read()
    
    assert sim_log.find("Hello World!") != -1
    
    pass

@pytest.mark.parametrize("sim", get_available_sims())
def test_simple_2(tmpdir, request,sim):
    data_dir = os.path.join(os.path.dirname(__file__), "data")
    runner = TaskSetRunner(os.path.join(tmpdir, 'rundir'))

    def marker_listener(marker):
        raise Exception("marker")

    builder = TaskGraphBuilder(
        PackageLoader(marker_listeners=[marker_listener]).load_rgy(['std', 'hdlsim.%s' % sim]),
        os.path.join(tmpdir, 'rundir'))

    top_v = builder.mkTaskNode(
        "std.FileSet",
        name="top_v",  
        type="systemVerilogSource", 
        base=data_dir, 
        include="*.v")

    sim_img_1 = builder.mkTaskNode(
        'hdlsim.%s.SimImage' % sim,
        name="sim_img_1", 
        needs=[top_v], 
        top=["top"])

    sim_img_2 = builder.mkTaskNode(
        'hdlsim.%s.SimImage' % sim,
        name="sim_img_2", 
        needs=[top_v], 
        top=["top"])

    sim_run_1 = builder.mkTaskNode(
        "hdlsim.%s.SimRun" % sim,
        name="sim_run_1", 
        needs=[sim_img_1])

    sim_run_2 = builder.mkTaskNode(
        "hdlsim.%s.SimRun" % sim,
        name="sim_run_2", 
        needs=[sim_img_2])

    runner.add_listener(TaskListenerLog().event)
    assert runner.status == 0
    out_l = asyncio.run(runner.run([sim_run_1, sim_run_2]))

    for out in out_l:
        rundir_fs = None
        for fs in out.output:
            if fs.type == 'std.FileSet' and fs.filetype == "simRunDir":
                rundir_fs = fs

        assert rundir_fs is not None
        assert rundir_fs.src in ("sim_run_1", "sim_run_2")

        assert os.path.isfile(os.path.join(rundir_fs.basedir, "sim.log"))
        with open(os.path.join(rundir_fs.basedir, "sim.log"), "r") as f:
            sim_log = f.read()
    
        assert sim_log.find("Hello World!") != -1

@pytest.mark.parametrize("sim", get_available_sims())
def test_passthrough_1(tmpdir, request,sim):

    data_dir = os.path.join(os.path.dirname(__file__), "data")
    runner = TaskSetRunner(os.path.join(tmpdir, 'rundir'))

    def marker_listener(marker):
        raise Exception("marker")

    builder = TaskGraphBuilder(
        PackageLoader(marker_listeners=[marker_listener]).load_rgy(['std', 'hdlsim.%s' % sim]),
        os.path.join(tmpdir, 'rundir'))

    mod1 = builder.mkTaskNode(
        'std.FileSet',
        name="mod1",  
        type="systemVerilogSource", 
        base=os.path.join(data_dir, "mod1"), include="*.sv")

    top_mod1 = builder.mkTaskNode(
        'std.FileSet',
        name="top_mod1", needs=[mod1], 
        type="systemVerilogSource", 
        base=os.path.join(data_dir, "top_mod1"), include="*.sv")

    sim_img = builder.mkTaskNode(
        'hdlsim.%s.SimImage' % sim,
        name="sim_img", needs=[top_mod1], top=["top"])

    sim_run = builder.mkTaskNode(
        'hdlsim.%s.SimRun' % sim,
        name="sim_run",
        needs=[sim_img])

    runner.add_listener(TaskListenerLog().event)
    out_l = asyncio.run(runner.run([sim_run]))

    for out in out_l:
        rundir_fs = None
        for fs in out.output:
            if fs.type == 'std.FileSet' and fs.filetype == "simRunDir":
                rundir_fs = fs

        assert rundir_fs is not None
        assert rundir_fs.src in ("sim_run",)

        assert os.path.isfile(os.path.join(rundir_fs.basedir, "sim.log"))
        with open(os.path.join(rundir_fs.basedir, "sim.log"), "r") as f:
            sim_log = f.read()
    
        assert sim_log.find("Hello World!") != -1

@pytest.mark.skip
@pytest.mark.parametrize("sim", get_available_sims())
def test_import_alias(tmpdir,sim):

    data_dir = os.path.join(os.path.dirname(__file__), "data")
    rgy = ExtRgy()
    rgy._discover_plugins()
    # rgy.registerPackage('hdlsim', 
    #                         os.path.join(hdlsim_path, "flow.dv"))
    # rgy.registerPackage('hdlsim.%s' % sim, 
    #                         os.path.join(hdlsim_path, "%s_flow.dv" % sim))

    flow_dv = """
package:
    name: foo

    imports:

"""
    flow_dv += "    - name: hdlsim.%s" % sim + "\n"
    flow_dv += "      as: hdlsim\n"

    flow_dv += """
    tasks:
    - name: files
      uses: std.FileSet
      with:
        type: systemVerilogSource
        include: "*.sv"
    - name: build
      uses: hdlsim.SimImage
      with:
        top: [top]
      needs: [files]
    - name: run
      uses: hdlsim.SimRun
      needs: [build]
"""

    with open(os.path.join(tmpdir, "flow.dv"), "w") as fp:
        fp.write(flow_dv)

    with open(os.path.join(tmpdir, "top.sv"), "w") as fp:
        fp.write("""
module top;
  initial begin
    $display("Hello World");
    $finish;
  end
endmodule
        """)

    pkg_def = loadProjPkgDef(os.path.join(tmpdir))

    builder = TaskGraphBuilder(
        pkg_def, 
        os.path.join(tmpdir, 'rundir'),
        pkg_rgy=rgy)

    runner = TaskGraphRunnerLocal(os.path.join(tmpdir, 'rundir'))
    
    run_t = builder.mkTaskGraph("foo.run")

    # hdlsim_path = os.path.dirname(
    #     os.path.abspath(libhdlsim.__file__))
    
    # fileset_t = builder.getTaskCtor(TaskSpec('std.FileSet'))
    # fileset_params = fileset_t.param_ctor()
    # fileset_params.type = "systemVerilogSource"
    # fileset_params.base = data_dir
    # fileset_params.include = "*.v"

    # top_v = fileset_t.mkTask(
    #     name="top_v",
    #     session=runner,
    #     params=fileset_params,
    #     rundir=os.path.join(tmpdir, "rundir", "top_v"),
    #     srcdir=fileset_t.srcdir
    # )
    
    # sim_img_t = builder.getTaskCtor(TaskSpec('hdlsim.%s.SimImage' % sim))
    # print("sim=%s sim_img_t.src=%s %s" % (sim, sim_img_t.srcdir, str(type(sim_img_t))))
    # sim_img_params = sim_img_t.mkParams()
    # sim_img_params.top.append('top')
    # sim_img = sim_img_t.mkTask(
    #     name="sim_img",
    #     session=runner,
    #     params=sim_img_params,
    #     rundir=os.path.join(tmpdir, "rundir", "sim_img"),
    #     srcdir=sim_img_t.srcdir,
    #     depends=[top_v]
    # )
    # print("sim: %s sim_img: %s" % (sim, str(type(sim_img))))

    # sim_run_t = builder.getTaskCtor(TaskSpec('hdlsim.%s.SimRun' % sim))
    # print("sim=%s sim_run_t.src=%s" % (sim, sim_run_t.srcdir))
    # sim_run = sim_run_t.mkTask(
    #     name="sim_run",
    #     session=runner,
    #     params=sim_run_t.mkParams(),
    #     rundir=os.path.join(tmpdir, "rundir", "sim_run"),
    #     srcdir=sim_run_t.srcdir,
    #     depends=[sim_img])

    # out = asyncio.run(runner.run(sim_run))

    # print("out: %s" % str(out))

    # rundir_fs = out.getFileSets("simRunDir")

    # assert len(rundir_fs) == 1
    # assert rundir_fs[0].src == "sim_run"

    # assert os.path.isfile(os.path.join(rundir_fs[0].basedir, "sim.log"))
    # with open(os.path.join(rundir_fs[0].basedir, "sim.log"), "r") as f:
    #     sim_log = f.read()
    
    # assert sim_log.find("Hello World!") != -1
    
    # pass
