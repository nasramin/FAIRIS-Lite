import xml.etree.ElementTree as ET

import pandas as pd


def parse_feeder(xml_feeder):
    fid = int(xml_feeder.get('id'))
    x = float(xml_feeder.get('x'))
    y = float(xml_feeder.get('y'))
    return pd.DataFrame(data=[[fid, x, y]], columns=['id', 'x', 'y'])


def parse_all_feeders(root):
    return pd.concat([pd.DataFrame(columns=['id', 'x', 'y'])] + [parse_feeder(xml_feeder) for xml_feeder in
                                                                 root.findall('feeder')]).reset_index(drop=True)


def parse_wall(xml_wall):
    data = [[float(xml_wall.get(coord)) for coord in ['x1', 'y1', 'x2', 'y2']]]
    return pd.DataFrame(data=data, columns=['x1', 'y1', 'x2', 'y2'])


def parse_all_obsticles(xml_root):
    return pd.concat([pd.DataFrame(columns=['x1', 'y1', 'x2', 'y2'])] + [parse_wall(xml_wall) for xml_wall in
                                                                         xml_root.findall('wall')]).reset_index(
        drop=True)


def parse_landmark(xml_landmark):
    data = [[float(xml_landmark.get(data)) for data in ['x', 'y', 'height', 'red', 'green', 'blue']]]
    return pd.DataFrame(data=data, columns=['x', 'y', 'height', 'red', 'green', 'blue'])


def parse_all_landmarks(xml_root):
    return pd.concat(
        [pd.DataFrame(columns=['x', 'y', 'height', 'red', 'green', 'blue'])] + [parse_landmark(xml_landmark) for xml_landmark in
                                                                      xml_root.findall('landmark')]).reset_index(
        drop=True)


def parse_position(xml_position):
    return pd.DataFrame(data=[[float(xml_position.get(p)) for p in ['x', 'y', 'theta']]], columns=['x', 'y', 'theta'])


def parse_start_positions(xml_positions):
    if xml_positions is None:
        return pd.DataFrame(columns=['x', 'y', 'theta'])
    return pd.concat([pd.DataFrame(columns=['x', 'y', 'theta'])] + [parse_position(xml_pos) for xml_pos in
                                                                xml_positions.findall('pos')]).reset_index(drop=True)


def parse_maze(file):
    root = ET.parse(file).getroot()
    start_positions = parse_start_positions(root.find('startPositions'))
    walls = parse_all_obsticles(root)
    feeders = parse_all_feeders(root)
    landmarks = parse_all_landmarks(root)

    return walls, feeders, start_positions, landmarks
