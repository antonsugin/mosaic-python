import sys
from PIL import Image
img = Image.open("im1.jpg")
import mosaic
pic = mosaic.build_tile_base('images',40)
pic1 = mosaic.load_image("im1.jpg")
from pprint import pprint


def compare_pixel(pixel1, pixel2):
    """This function calculates distance between 2 pixels"""

    distance_between_pixels = (
                (abs(pixel1[0] - pixel2[0])) + (abs(pixel1[1] - pixel2[1])) + (abs(pixel1[2] - pixel2[2])))
    return distance_between_pixels


def compare(image1, image2):
    """This function calculates distance between images"""

    distance_between_images = 0
    for i in range(min(len(image1), len(image2))):
        for j in range(min(len(image1[0]), len(image2[0]))):
            distance_between_images += compare_pixel(image1[i][j], image2[i][j])
    return distance_between_images


def get_piece(image, upper_left, size):
    """This function returns a section from a picture"""

    pieces = []
    col = upper_left[0]
    row = upper_left[1]
    for i in range(col, min(len(image), size[0] + col)):
        pieces_temp = []
        for j in range(row, min(len(image[0]), size[1] + row)):
            pieces_temp.append(image[i][j])
            pieces.append(pieces_temp)
    return pieces


def set_piece(image, upper_left, piece):
    """This function replaces a certain segment of the picture given in pixels from another image"""

    col = upper_left[0]
    row = upper_left[1]
    for i in range(col, min(len(image), len(piece) + col)):
        for j in range(row, min(len(image[0]), len(piece[0]) + row)):
            image[i][j] = piece[i-col][j-row]


def average(image):
    """This function calculates the average color of the pixels"""

    r, g, b = 0, 0, 0
    row = len(image)
    col = len(image[0])
    num_of_pix = row * col
    for i in range(len(image)):
        for j in range(len(image[0])):
            r += image[i][j][0]
            g += image[i][j][1]
            b += image[i][j][2]
    r_average = r / num_of_pix
    g_average = g / num_of_pix
    b_average = b / num_of_pix
    return (int(r_average), int(g_average), int(b_average))


def preprocess_tiles(tiles):
    """This function returns a list of tiles, with the average colors for each tile"""

    tile = []
    for i in tiles:
        tile.append(average(i))
    return tile


def get_best_tiles(objective, tiles, averages , num_candidates):
    """This function returns a list of tiles whose average pixel color is similar
        the average pixel color of a goal image"""

    tiles1 = []
    average_tile = average(objective)
    for i in range(num_candidates):
        tiles1.append(0)
        pixel_average = 255
        for j in range(len(averages)):
            if compare_pixel(average_tile, averages[j]) < pixel_average:
                ind = j
                pixel_average = compare_pixel(average_tile, averages[ind])
        tiles1[i] = tiles[ind]
    return tiles1


def choose_tile(piece, tiles):
    """This function returns the most suitable tile from a list of tiles"""

    ind = 0
    tile2 = compare(piece, tiles[0])
    for i in range(1, len(tiles)):
        tile3 = compare(piece, tiles[i])
        if tile2 > tile3:
            tile2 = tile3
            ind = i
    return tiles[ind]


def make_mosaic(image, tiles, num_candidates):
    """This function creates a Photomosaic image"""

    col = len(tiles[0][0])
    row = len(tiles[0])
    average_tiles = preprocess_tiles(tiles)
    for i in range(0, len(image), row):
        for j in range(0, len(image[0]), col):
            piece = get_piece(image, (i, j), (row, col))
            tiles_list = get_best_tiles(piece, tiles, average_tiles, num_candidates)
            most_suit_tile = choose_tile(piece, tiles_list)
            set_piece(image, (i, j), most_suit_tile)
    return image


z = make_mosaic(pic1, pic, 40)
mosaic.show(z)

