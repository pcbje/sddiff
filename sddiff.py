#!/usr/bin/env python
"""
This work is made available under the Apache License, Version 2.0.

You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
License for the specific language governing permissions and limitations under
the License.

Based on the work of Vassil Roussev and Candice Quates (http://sdhash.org)
"""
import sys
import os
import math
import struct
import pyx

WINDOW_SIZE = 64
BINS = 1000;
ENTR_POWER = 10;
ENTR_SCALE = (BINS * (1 << ENTR_POWER));
ENTROPY_64_INT = [0]*65
ENTR64_RANKS = [
  000, 000, 000, 000, 000, 000, 000, 000, 000, 000, 000, 000, 000, 000, 000, 000, 000, 000, 000, 000,
  000, 000, 000, 000, 000, 000, 000, 000, 000, 000, 000, 000, 000, 000, 000, 000, 000, 000, 000, 000,
  000, 000, 000, 000, 000, 000, 000, 000, 000, 000, 000, 000, 000, 000, 000, 000, 000, 000, 000, 000,
  000, 000, 000, 000, 000, 000, 000, 000, 000, 000, 000, 000, 000, 000, 000, 000, 000, 000, 000, 000,
  000, 000, 000, 000, 000, 000, 000, 000, 000, 000, 000, 000, 000, 000, 000, 000, 000, 000, 000, 000,
  101, 102, 106, 112, 108, 107, 103, 100, 109, 113, 128, 131, 141, 111, 146, 153, 148, 134, 145, 110,
  114, 116, 130, 124, 119, 105, 104, 118, 120, 132, 164, 180, 160, 229, 257, 211, 189, 154, 127, 115,
  129, 142, 138, 125, 136, 126, 155, 156, 172, 144, 158, 117, 203, 214, 221, 207, 201, 123, 122, 121,
  135, 140, 157, 150, 170, 387, 390, 365, 368, 341, 165, 166, 194, 174, 184, 133, 139, 137, 149, 173,
  162, 152, 159, 167, 190, 209, 238, 215, 222, 206, 205, 181, 176, 168, 147, 143, 169, 161, 249, 258,
  259, 254, 262, 217, 185, 186, 177, 183, 175, 188, 192, 195, 182, 151, 163, 199, 239, 265, 268, 242,
  204, 197, 193, 191, 218, 208, 171, 178, 241, 200, 236, 293, 301, 256, 260, 290, 240, 216, 237, 255,
  232, 233, 225, 210, 196, 179, 202, 212, 420, 429, 425, 421, 427, 250, 224, 234, 219, 230, 220, 269,
  247, 261, 235, 327, 332, 337, 342, 340, 252, 187, 223, 198, 245, 243, 263, 228, 248, 231, 275, 264,
  298, 310, 305, 309, 270, 266, 251, 244, 213, 227, 273, 284, 281, 318, 317, 267, 291, 278, 279, 303,
  452, 456, 453, 446, 450, 253, 226, 246, 271, 277, 295, 302, 299, 274, 276, 285, 292, 289, 272, 300,
  297, 286, 314, 311, 287, 283, 288, 280, 296, 304, 308, 282, 402, 404, 401, 415, 418, 313, 320, 307,
  315, 294, 306, 326, 321, 331, 336, 334, 316, 328, 322, 324, 325, 330, 329, 312, 319, 323, 352, 345,
  358, 373, 333, 346, 338, 351, 343, 405, 389, 396, 392, 411, 378, 350, 388, 407, 423, 419, 409, 395,
  353, 355, 428, 441, 449, 474, 475, 432, 457, 448, 435, 462, 470, 467, 468, 473, 426, 494, 487, 506,
  504, 517, 465, 459, 439, 472, 522, 520, 541, 540, 527, 482, 483, 476, 480, 721, 752, 751, 728, 730,
  490, 493, 495, 512, 536, 535, 515, 528, 518, 507, 513, 514, 529, 516, 498, 492, 519, 508, 544, 547,
  550, 546, 545, 511, 532, 543, 610, 612, 619, 649, 691, 561, 574, 591, 572, 553, 551, 565, 597, 593,
  580, 581, 642, 578, 573, 626, 696, 584, 585, 595, 590, 576, 579, 583, 605, 569, 560, 558, 570, 556,
  571, 656, 657, 622, 624, 631, 555, 566, 564, 562, 557, 582, 589, 603, 598, 604, 586, 577, 588, 613,
  615, 632, 658, 625, 609, 614, 592, 600, 606, 646, 660, 666, 679, 685, 640, 645, 675, 681, 672, 747,
  723, 722, 697, 686, 601, 647, 677, 741, 753, 750, 715, 707, 651, 638, 648, 662, 667, 670, 684, 674,
  693, 678, 664, 652, 663, 639, 680, 682, 698, 695, 702, 650, 676, 669, 665, 688, 687, 701, 700, 706,
  683, 718, 703, 713, 720, 716, 735, 719, 737, 726, 744, 736, 742, 740, 739, 731, 711, 725, 710, 704,
  708, 689, 729, 727, 738, 724, 733, 692, 659, 705, 654, 690, 655, 671, 628, 634, 621, 616, 630, 599,
  629, 611, 620, 607, 623, 618, 617, 635, 636, 641, 637, 633, 644, 653, 699, 694, 714, 734, 732, 746,
  749, 755, 745, 757, 756, 758, 759, 761, 763, 765, 767, 771, 773, 774, 775, 778, 782, 784, 786, 788,
  793, 794, 797, 798, 803, 804, 807, 809, 816, 818, 821, 823, 826, 828, 829, 834, 835, 839, 843, 846,
  850, 859, 868, 880, 885, 893, 898, 901, 904, 910, 911, 913, 916, 919, 922, 924, 930, 927, 931, 938,
  940, 937, 939, 941, 934, 936, 932, 933, 929, 928, 926, 925, 923, 921, 920, 918, 917, 915, 914, 912,
  909, 908, 907, 906, 900, 903, 902, 905, 896, 899, 897, 895, 891, 894, 892, 889, 883, 890, 888, 879,
  887, 886, 882, 878, 884, 877, 875, 872, 876, 870, 867, 874, 873, 871, 869, 881, 863, 865, 864, 860,
  853, 855, 852, 849, 857, 856, 862, 858, 861, 854, 851, 848, 847, 845, 844, 841, 840, 837, 836, 833,
  832, 831, 830, 827, 824, 825, 822, 820, 819, 817, 815, 812, 814, 810, 808, 806, 805, 799, 796, 795,
  790, 787, 785, 783, 781, 777, 776, 772, 770, 768, 769, 764, 762, 760, 754, 743, 717, 712, 668, 661,
  643, 627, 608, 594, 587, 568, 559, 552, 548, 542, 539, 537, 534, 533, 531, 525, 521, 510, 505, 497,
  496, 491, 486, 485, 478, 477, 466, 469, 463, 458, 460, 444, 440, 424, 433, 403, 410, 394, 393, 385,
  377, 379, 382, 383, 380, 384, 372, 370, 375, 366, 354, 363, 349, 357, 347, 364, 367, 359, 369, 360,
  374, 344, 376, 335, 371, 339, 361, 348, 356, 362, 381, 386, 391, 397, 399, 398, 412, 408, 414, 422,
  416, 430, 417, 434, 400, 436, 437, 438, 442, 443, 447, 406, 451, 413, 454, 431, 455, 445, 461, 464,
  471, 479, 481, 484, 489, 488, 499, 500, 509, 530, 523, 538, 526, 549, 554, 563, 602, 596, 673, 567,
  748, 575, 766, 709, 779, 780, 789, 813, 811, 838, 842, 866, 942, 935, 944, 943, 947, 952, 951, 955,
  954, 957, 960, 959, 967, 966, 969, 962, 968, 953, 972, 961, 982, 979, 978, 981, 980, 990, 987, 988,
  984, 983, 989, 985, 986, 977, 976, 975, 973, 974, 970, 971, 965, 964, 963, 956, 958, 524, 950, 948,
  949, 945, 946, 800, 801, 802, 791, 792, 501, 502, 503, 000, 000, 000, 000, 000, 000, 000, 000, 000,
  000
]

for i in range(1, WINDOW_SIZE + 1):
  p = float(i) / WINDOW_SIZE	
  ENTROPY_64_INT[i] = int((-p * math.log(p, 2) / 6) * ENTR_SCALE)

class Sdfeature(object):	
  def __init__(self, path):
    self.input = open(path, "rb")
    self.ascii = [0] * 256
    self.window = bytearray([0] * WINDOW_SIZE)
    self.previous_entropy = 0
    self.position = 0

  def close(self):
    self.input.close()

  def next(self):
    next_byte = self.input.read(1)

    if not next_byte:
      return -1

    self.position += 1

    drop_char = self.window.pop(0)

    if self.ascii[drop_char] > 0:
      self.ascii[drop_char] -= 1;
      old_diff = ENTROPY_64_INT[self.ascii[drop_char] + 1] - ENTROPY_64_INT[self.ascii[drop_char]];           
    else:
      old_diff = 0

    next_char = struct.unpack('B', next_byte)[0]				
    self.window.append(next_char)

    self.ascii[next_char] += 1;

    new_diff = ENTROPY_64_INT[self.ascii[next_char]] - ENTROPY_64_INT[self.ascii[next_char] - 1]

    entropy = self.previous_entropy - old_diff + new_diff

    self.previous_entropy = entropy
		
    return ENTR64_RANKS[int(entropy) >> ENTR_POWER]

  def getFeatures(self, callback):
    score = 0
    max_score = 0		
    max_index = 0
    popularity = [0] * WINDOW_SIZE	
    scores = [0] * WINDOW_SIZE
    counts = [0] * WINDOW_SIZE
    windows = [{}] * WINDOW_SIZE
		
    while score >= 0:
      score = self.next()

      current_index = self.position % WINDOW_SIZE

      scores[current_index] = score
      counts[current_index] = 0;

      windows[current_index] = {
        'position': self.position,
        'bytes': self.window
      }
			
      if score > max_score:
        max_score = score
        max_index = current_index
      elif current_index == max_index and self.position >= WINDOW_SIZE:
        max_index = 0
        max_score = 0

        for j in range(current_index, current_index + WINDOW_SIZE):
          if scores[j % WINDOW_SIZE] > max_score:
            max_score = scores[j % WINDOW_SIZE]
            max_index = j % WINDOW_SIZE
			
      counts[max_index] += 1

      if self.position >= WINDOW_SIZE and counts[max_index] == 10:
        callback(windows[max_index])

    return self

class Sddiff(object):
  def diff(self, path1, path2, slots=400):
    len1 = os.path.getsize(path1)
    len2 = os.path.getsize(path2)

    if len1 > len2:
      tmp = path1
      path1 = path2
      path2 = tmp

    self.references = {}
    self.result = [0] * slots
    self.divident = max(1, float(os.path.getsize(path2)) / len(self.result));
    self.feature_count = 0

    Sdfeature(path1).getFeatures(self.addToReferences).close()
    Sdfeature(path2).getFeatures(self.compare).close()

  def addToReferences(self, feature):
    self.references[str(feature['bytes'])] = feature['position']

  def compare(self, feature):
    position = int(feature['position'] / self.divident)

    if str(feature['bytes']) in self.references:
      self.result[position] = 1
    elif self.result[position] == 0:
      self.result[position] = -1

    self.feature_count += 1

  def save(self, path, ratio=0.1):
    canvas = pyx.canvas.canvas()
    step = 0.2
    height = float(len(self.result)) * step * ratio		    
    factor = len(self.result) / min(self.feature_count, len(self.result))

    pos = step * 2

    for res in self.result:
      color = self.getColor(res)			
      if color != None:
        for x in range(0, factor):
          canvas.stroke(pyx.path.line(pos,step * 1.5,pos,height), [pyx.style.linewidth(step), color])
          pos += step

    # Bottom horizontal
    canvas.stroke(pyx.path.line(0,0,pos + step,0), [pyx.style.linewidth(step / 2), pyx.color.rgb.black])

    # Top horizontal
    canvas.stroke(pyx.path.line(0, height + (step * 1.5), pos + step, height + (step * 1.5)), [pyx.style.linewidth(step / 2), pyx.color.rgb.black])

    # Left vertical
    canvas.stroke(pyx.path.line(0,0,0,height + (step * 1.5)), [pyx.style.linewidth(step / 2), pyx.color.rgb.black])

    # Right vertical
    canvas.stroke(pyx.path.line(pos + step,0,pos + step, height + (step * 1.5)), [pyx.style.linewidth(step / 2), pyx.color.rgb.black])

    canvas.writeGSfile(path)

  def getColor(self, value):
    if value == -1:
      return pyx.color.rgb.white
    elif value == 1:
      return pyx.color.rgb.blue        

    return None

if __name__ == '__main__':
  sddiff = Sddiff()
  sddiff.diff(sys.argv[1], sys.argv[2])
  sddiff.save(sys.argv[3])
