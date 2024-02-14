     cv.rectangle(img, (x + 2, y + 2), (x + w - 2, y + h - 2), (175,8,175), cv.FILLED) 
                                    cv.putText(img, button.text, (x + 20, y + 55), cv.FONT_HERSHEY_PLAIN, 3, (255, 255, 255), 3)
                                    finaltext=finaltext+button.text