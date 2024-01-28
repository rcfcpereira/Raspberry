# #########################################
# #LCD 16x2
# # I2C addresses
# bus = smbus.SMBus(1)
# DISPLAY_TEXT_ADDR = 0x3e

# # send command to display (no need for external use)
# def textCommand(cmd):
#     bus.write_byte_data(DISPLAY_TEXT_ADDR,0x80,cmd)

# # set display text \n for second line(or auto wrap)
# def setText(text):
#     textCommand(0x01) # clear display
#     time.sleep(.05)
#     textCommand(0x08 | 0x04) # display on, no cursor
#     textCommand(0x28) # 2 lines
#     time.sleep(.05)
#     count = 0
#     row = 0
#     for c in text:
#         if c == '\n' or count == 16:
#             count = 0
#             row += 1
#             if row == 2:
#                 break
#             textCommand(0xc0)
#             if c == '\n':
#                 continue
#         count += 1
#         bus.write_byte_data(DISPLAY_TEXT_ADDR,0x40,ord(c))

# #Update the display without erasing the display
# def setText_norefresh(text):
#     textCommand(0x02) # return home
#     time.sleep(.05)
#     textCommand(0x08 | 0x04) # display on, no cursor
#     textCommand(0x28) # 2 lines
#     time.sleep(.05)
#     count = 0
#     row = 0
#     while len(text) < 32: #clears the rest of the screen
#         text += ' '
#     for c in text:
#         if c == '\n' or count == 16:
#             count = 0
#             row += 1
#             if row == 2:
#                 break
#             textCommand(0xc0)
#             if c == '\n':
#                 continue
#         count += 1
#         bus.write_byte_data(DISPLAY_TEXT_ADDR,0x40,ord(c)),,