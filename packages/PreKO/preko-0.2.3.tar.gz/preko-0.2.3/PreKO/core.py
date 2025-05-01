import os, re, sys, logging
import subprocess as sp
import numpy as np

from pdb import set_trace

# CRISPResso 설치 필수
from CRISPResso2 import CRISPResso2Align


class CoreHash(object):

    @staticmethod
    def MakeHashList(strSeq, intBarcodeLen):
        listSeqWindow = [strSeq[i:i + intBarcodeLen] for i in range(len(strSeq))[:-intBarcodeLen - 1]]
        return listSeqWindow

    @staticmethod
    def IndexHashList(dictRef, strSeqWindow):
        lCol_ref = dictRef[strSeqWindow]
        strBarcode = strSeqWindow

        return (lCol_ref, strBarcode)


class CoreGotoh(object):

    def __init__(self, strEDNAFULL='', floOg='', floOe=''):
        self.npAlnMatrix = CRISPResso2Align.read_matrix(strEDNAFULL)
        self.floOg       = floOg
        self.floOe       = floOe
    
    def GapIncentive(self, strRefSeqAfterBarcode):
        ## cripsress no incentive == gotoh
        intAmpLen = len(strRefSeqAfterBarcode)
        npGapIncentive = np.zeros(intAmpLen + 1, dtype=np.int_) # intAmpLen range: < 500nt
        return npGapIncentive

    def RunCRISPResso2(self, strQuerySeqAfterBarcode, strRefSeqAfterBarcode, npGapIncentive):
        listResult = CRISPResso2Align.global_align(strQuerySeqAfterBarcode.upper(), strRefSeqAfterBarcode.upper(),
                                                  matrix=self.npAlnMatrix, gap_open=self.floOg, gap_extend=self.floOe,
                                                  gap_incentive=npGapIncentive)
        return listResult


class Helper(object):

    @staticmethod
    def MakeFolderIfNot(strDir):
        if not os.path.isdir(strDir): os.makedirs(strDir)

    @staticmethod
    def RemoveNullAndBadKeyword(Sample_list):
        listSamples = [strRow for strRow in Sample_list.readlines() if strRow not in ["''", '', '""', '\n', '\r', '\r\n']]
        return listSamples

    @staticmethod ## defensive
    def CheckSameNum(strInputProject, listSamples):

        listProjectNumInInput = [i for i in sp.check_output('ls %s' % strInputProject, shell=True).split('\n') if i != '']

        setSamples           = set(listSamples)
        setProjectNumInInput = set(listProjectNumInInput)

        intProjectNumInTxt    = len(listSamples)
        intProjectNumInInput  = len(listProjectNumInInput)

        if intProjectNumInTxt != len(setSamples - setProjectNumInInput):
            logging.warning('The number of samples in the input folder and in the project list does not matched.')
            logging.warning('Input folder: %s, Project list samples: %s' % (intProjectNumInInput, intProjectNumInTxt))
            raise AssertionError
        else:
            logging.info('The file list is correct, pass\n')

    @staticmethod ## defensive
    def CheckAllDone(strOutputProject, listSamples):
        intProjectNumInOutput = len([i for i in sp.check_output('ls %s' % strOutputProject, shell=True).split('\n') if i not in ['All_results', 'Log', '']])

        if intProjectNumInOutput != len(listSamples):
            logging.warning('The number of samples in the output folder and in the project list does not matched.')
            logging.warning('Output folder: %s, Project list samples: %s\n' % (intProjectNumInOutput, len(listSamples)))
        else:
            logging.info('All output folders have been created.\n')

    @staticmethod
    def SplitSampleInfo(strSample):

        if strSample[0] == '#': return False
        logging.info('Processing sample : %s' % strSample)
        lSampleRef = strSample.replace('\n', '').replace('\r', '').replace(' ', '').split('\t')

        if len(lSampleRef) == 2:
            strSample = lSampleRef[0]
            strRef = lSampleRef[1]
            return (strSample, strRef, '')

        elif len(lSampleRef) == 3:
            strSample = lSampleRef[0]
            strRef = lSampleRef[1]
            strExpCtrl = lSampleRef[2].upper()
            return (strSample, strRef, strExpCtrl)

        else:
            logging.error('Confirm the file format is correct. -> Sample name\tReference name\tGroup')
            logging.error('Sample list input : %s\n' % lSampleRef)
            raise Exception

    @staticmethod
    def CheckIntegrity(strBarcodeFile, strSeq): ## defensive
        rec = re.compile(r'[A|C|G|T|N]')

        if ':' in strSeq:
            strSeq = strSeq.split(':')[1]

        strNucle = re.findall(rec, strSeq)
        if len(strNucle) != len(strSeq):
            logging.error('This sequence is not suitable, check A,C,G,T,N are used only : %s' % strBarcodeFile)
            set_trace()
            sys.exit(1)

    @staticmethod
    def PreventFromRmMistake(strCmd):
        rec = re.compile(r'rm.+-rf*.+(\.$|\/$|\*$|User$|Input$|Output$)') ## This reg can prevent . / * ./User User ...
        if re.findall(rec, strCmd):
            raise Exception('%s is critical mistake! never do like this.' % strCmd)


def CheckProcessedFiles(Func):
    def Wrapped_func(**kwargs):

        InstInitFolder     = kwargs['InstInitFolder']
        strInputProject    = kwargs['strInputProject']
        listSamples        = kwargs['listSamples']
        logging            = kwargs['logging']

        logging.info('File num check: input folder and project list')
        Helper.CheckSameNum(strInputProject, listSamples)

        Func(**kwargs)

        logging.info('Check that all folder are well created.')
        Helper.CheckAllDone(InstInitFolder.strOutputProjectDir, listSamples)

    return Wrapped_func


def AttachSeqToIndel(strSample, strBarcodeName, strIndelPos,
                     strRefseq, strQueryseq, dictSub):

    listIndelPos = strIndelPos.split('M')
    intMatch     = int(listIndelPos[0])

    if 'I' in strIndelPos:
        intInsertion    = int(listIndelPos[1].replace('I', ''))
        strInDelSeq     = strQueryseq[intMatch:intMatch + intInsertion]

    elif 'D' in strIndelPos:
        intDeletion     = int(listIndelPos[1].replace('D', ''))
        strInDelSeq    = strRefseq[intMatch:intMatch + intDeletion]

    else:
        logging.info('strIndelClass is included I or D. This variable is %s' % strIndelPos)
        raise Exception

    strInDelPosSeq = strIndelPos + '_' + strInDelSeq

    try:
        _ = dictSub[strSample][strBarcodeName]
    except KeyError:
        dictSub[strSample][strBarcodeName] = {}

    try:
        dictSub[strSample][strBarcodeName][strBarcodeName + ':' + strInDelPosSeq]['IndelCount'] += 1
    except KeyError:
        dictSub[strSample][strBarcodeName][strBarcodeName + ':' + strInDelPosSeq] = {'IndelCount':1}


