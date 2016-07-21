#!/usr/bin/python
import os, argparse, glob, os, sys
from lxml import etree
from pymicmac import utils_execution

def run(dataDir, configFile, setEnvironmentFileToSource, remoteExeDir, localOutDir, qsuboptions, qsubScript):

    e = etree.parse(configFile).getroot()
    numComponents = len(e.findall('Component'))

    scriptsParentPath = os.path.dirname(os.path.realpath(__file__))
    executable = scriptsParentPath + '/run_distributed_workflow_sge_job.sh'
    executable_python = scriptsParentPath + '/run_distributed_workflow_sge_job.py'

    configFileAbsPath = os.path.abspath(configFile)
    dataDirAbsPath = os.path.abspath(dataDir)
    localOutDirAbsPath = os.path.abspath(localOutDir)

    if os.path.isfile(qsubScript):
        raise Exception(qsubScript + ' already exists!')

    ofile = open(qsubScript, 'w')
    for i in range(numComponents):
        ofile.write('qsub ' + qsuboptions + ' ' + executable + ' ' + setEnvironmentFileToSource + ' ' + executable_python + ' ' + configFileAbsPath + ' ' + str(i) + ' ' + dataDirAbsPath + ' ' + remoteExeDir + ' ' + localOutDirAbsPath + '\n')
    ofile.close()

def argument_parser():
   # define argument menu
    description = "Creates the jobs to submit to a SGE cluster for a MicMac XML distributed computing workflow. For each executed command there is monitoring of used CPU/MEM/disk."
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('-d', '--dataDir',default='', help='Data directory with the required data and the distribution configuration folder (this has to be shared and accessible from the cluster nodes)', type=str, required=True)
    parser.add_argument('-c', '--configFile',default='', help='Distributed Tool XML configuration file with the several commands that will be executed in parallel through in SGE cluster. This file must be in the data directory', type=str, required=True)
    parser.add_argument('-s', '--source',default='', help='Set environment file (this file is sourced before the remote execution of any command, the file must be in a shared folder and be accessible from the cluster nodes)', type=str, required=True)
    parser.add_argument('-r', '--remoteExeDir',default='', help='Remote execution directory. Each command will be executed in a cluster node in a folder like <remoteExeDir>/<commandId>', type=str, required=True)
    parser.add_argument('-o', '--localOutDir',default='', help='Local output folder. The execution of each command of the workflow will be done in a remote folder in a SGE node, but the output specified in the configuration XML will be copied to a local folder <localOutDir>/<commandId>', type=str, required=True)
    parser.add_argument('-q', '-qsubScript',default='', help='Output file that will contain the different qsubs commands. Execution this file will lunch (add to processing queue) the different commands in the SGE cluster', type=str, required=True)
    parser.add_argument('--qsuboptions',default='-l h_rt=00:15:00 -N disttool', help='Options to pass to qsub command. At least must include a -N <name> [default is "-l h_rt=00:15:00 -N disttool"]', type=str, required=False)
    return parser

if __name__ == "__main__":
    try:
        a = utils_execution.apply_argument_parser(argument_parser())
        run(a.dataDir, a.configFile, a.source, a.remoteExeDir, a.localOutDir, a.qsuboptions, a.qsubScript)
    except Exception as e:
        print(e)