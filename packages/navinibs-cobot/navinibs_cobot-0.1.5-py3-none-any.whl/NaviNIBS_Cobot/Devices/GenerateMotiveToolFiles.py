
import fileinput
from shutil import copy
from os import path
from pathlib import Path
from uuid import uuid4
import numpy as np
from base64 import b64encode
import argparse
from struct import pack, unpack
import pathlib


from NaviNIBS.util.Transforms import applyTransform, concatenateTransforms, invertTransform, composeTransform

def decodeNDIROM(romPath):
    with open(romPath, 'rb') as f:
        rawRom = f.read()

    print('***** Raw ******')
    print(rawRom)

    print('\n**** uint8 ****')
    for i, byte in enumerate(rawRom):
        print(f'{i}: {byte}')

    # (determined empirically, may be incorrect for some files)
    numMarkers = rawRom[28]  # TODO: determine if this is byte 28 or 32

    for byteOffset in range(0,1):
        print('\n**** Single byteOffset=%d ****' % byteOffset)
        for i, byteStart in enumerate(range(byteOffset, len(rawRom)-4, 4)):
            num, = unpack('<f', rawRom[byteStart:byteStart+4])
            if num != 0.0 or True:
                print(f'{i}: {num}')


    for byteStart in range(byteOffset, len(rawRom)-4, 4):
        s = [unpack('c', rawRom[iB:iB+1])[0] for iB in range(byteStart, byteStart+4)]
        print([c if int.from_bytes(c) < 128 and c.decode('ascii').isalnum() else '' for c in s])

    bytesPerVal = 4
    coordinateBytes = rawRom[72:(72+numMarkers*bytesPerVal*3)]
    coordinates = np.zeros((numMarkers, 3))
    for iM in range(numMarkers):
        for iXYZ in range(3):
            startIndex = iM*bytesPerVal*3 + iXYZ*bytesPerVal
            print(startIndex)
            coordinates[iM, iXYZ] = unpack('<f', coordinateBytes[startIndex:(startIndex+bytesPerVal)])[0]

    return coordinates


def formatMarkerCoordinatesForMotive(coords: np.ndarray) -> str:
    s = '<markers>'
    for iMarker, coord in enumerate(coords):
        s += '\n\t<marker active_id="0">'
        s += '\n\t\t<position>'
        for iXYZ, xyz in enumerate(coord):
            s += f'{xyz/1e3:f}'
            if iXYZ < 2:
                s += ', '
        s += '</position>'
        s += '\n\t\t<size>0.02</size>'
        s += f'\n\t\t<label_id>{iMarker+1}</label_id>'
        s += '\n\t</marker>'
    s += '\n</markers>'
    return s


def generateCartTrackerToolFile():
    thisDir = pathlib.Path(__file__)

    inputPath = '../resources/Axilum-TMS-Cobot-Right-World.rom'
    rightCoords_rightTrackerSpace = decodeNDIROM(thisDir/inputPath)

    inputPath = '../resources/Axilum-TMS-Cobot-Left-World.rom'
    leftCoords_leftTrackerSpace = decodeNDIROM(thisDir / inputPath)

    # based on Axilum calibration data for Cobot SN SW0047:
    transf_cartToRightTracker = np.asarray([
        [0.011904022479658, -0.999928993370481,   0.000549968998558,   0.312540000000000],
        [0.999927432943067,   0.011902982626364, -0.001856839380730,   0.205759000000000],
        [0.001850161261390,   0.000572032946656,   0.999998124839049,  0.060532000000000],
        [0,                   0,                   0,                  1.000000000000000]])

    transf_cartToLeftTracker = np.asarray([
        [0.016285825819013, -0.999783999542953, -0.012912247491815,  0.310272000000000],
        [0.999867279385931,  0.016290176753010, -0.000231850665680, -0.213382000000000],
        [0.000442143379750, -0.012906757890841,   0.999916606577758, 0.065709000000000],
        [0,                   0,                   0,                1.000000000000000]])

    # convert from m to mm
    transf_cartToLeftTracker[0:3, 3] *= 1e3
    transf_cartToRightTracker[0:3, 3] *= 1e3

    leftCoords_cartSpace = applyTransform(invertTransform(transf_cartToLeftTracker), leftCoords_leftTrackerSpace)
    rightCoords_cartSpace = applyTransform(invertTransform(transf_cartToRightTracker), rightCoords_rightTrackerSpace)

    leftCoords_rightTrackerSpace = applyTransform(concatenateTransforms([invertTransform(transf_cartToLeftTracker), transf_cartToRightTracker]),
                                                  leftCoords_leftTrackerSpace)

    # print marker positions in format for motive asset definition
    allCoords_rightTrackerSpace = np.concatenate((leftCoords_rightTrackerSpace, rightCoords_rightTrackerSpace), 0)

    s = formatMarkerCoordinatesForMotive(allCoords_rightTrackerSpace)
    print(s)


def generateCalibrationPlateToolFile():
    origCoordinates = np.asarray([
        [10, 10, 7],  # marker 1
        [210, 10, 7],  # marker 2
        [10, 160, 7],  # marker 3
        [63.823, 63.823, 0],  # CB60 coil origin (according to 3d-printed jig v1.0)
        [68.914, 68.914, 0],  # B65 AP CO coil origin (according to 3d-printed jig v1.1
        [40.4, 40.4, 0], # 1/4-20 threaded hole used for thumbscrew to align upper part of coil figure 8
    ])

    import pytransform3d.rotations as ptr
    rot = ptr.active_matrix_from_angle(2, -3*np.pi/4)
    transf_rot = composeTransform(rot)
    rotCoordinates = applyTransform(transf_rot, origCoordinates)

    if False:
        newCoordinates_screw = rotCoordinates - rotCoordinates[-1, :]  # make the 1/4-20 threaded hole the origin
    else:
        newCoordinates_screw = rotCoordinates  # keep the original origin of calibration plate

    yOffset_B65APCO = -40.3251
    yOffset_CB60 = 33.1251

    newCoordinates_B65APCO = newCoordinates_screw + np.asarray([0, yOffset_B65APCO, 0])
    newCoordinates_CB60 = newCoordinates_screw + np.asarray([0, yOffset_CB60, 0])

    markerCoordinates_B65APCO = newCoordinates_B65APCO[:-3, :]
    markerCoordinates_CB60 = newCoordinates_CB60[:-3, :]

    print('****** Calibration plate ******')
    print(formatMarkerCoordinatesForMotive(newCoordinates_screw))

    print('****** CB60 ******')
    print(formatMarkerCoordinatesForMotive(markerCoordinates_CB60))

    print('****** B65APCO ******')
    print(formatMarkerCoordinatesForMotive(markerCoordinates_B65APCO[:-3, :]))

    print('todo')


if __name__ == '__main__':
    print('**** Cart tracker ****')
    generateCartTrackerToolFile()


    print('**** Calibration plate ****')
    generateCalibrationPlateToolFile()