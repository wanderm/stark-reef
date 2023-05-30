def correctSubtitleEncoding(filename, newFilename, encoding_from, encoding_to='UTF-8'):
    with open(filename, 'r', encoding=encoding_from) as fr:
        with open(newFilename, 'w', encoding=encoding_to) as fw:
            for line in fr:
                fw.write(line[:-1]+'\r\n')

correctSubtitleEncoding('./wraw_data/2020-09_Brazil_data.csv', './wraw_data/aaa.csv', 'us-ascii', encoding_to='utf-8')
