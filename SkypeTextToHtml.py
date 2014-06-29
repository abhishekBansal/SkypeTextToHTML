# -*- coding: utf-8 -*-
"""
Created on Sun Sep 08 23:18:17 2013

@author: Abhishek Bansal

@todo:  1. Format as close as skype chat environment
        2. Handle quotes
        3. Add support for emoticons, preferably gifs
        4. Test for group chats
        5. Group by date - dont add date with every message - done
        6. Omit repeated usernames as in skype - done
"""
import os

class SkypeTextToHtml:
    

    def __init__(self):
        
        #maintains handle to output HTML file
        self.outputFileHandle = None
        self.inputFileHandle = None
        self.userList = []
        self.prevUserName = None
        self.prevDate = None
    
    def writeHeader(self, title):
        
        outputFileHeader = "<html> <head> <link rel=\"stylesheet\" type=\"text/css\" href=\"bubbles.css\"> <title>" + title + "</title> </head> <body>"
        tableHeader = "<table align=\"center\" width: 1000 style=\"table-layout: fixed;\">"
        self.outputFileHandle.write(outputFileHeader + tableHeader)
        
    
    def writeFooter(self):
        
        tableFooter = "</table>"
        outputFileFooter = "</body> </html>"
        self.outputFileHandle.write(tableFooter + outputFileFooter)
        
    
    def getTimeStamp(self, line):
        
        #try to extract timestamp
        index = line.find("]")
        if -1 == index:
            return None
        else:
            fullTimeStamp = line[1:index]
            spaceIndex = fullTimeStamp.find(' ')
            datePart = fullTimeStamp[0:spaceIndex]
            timePart = fullTimeStamp[spaceIndex+1:]
            
            return [datePart, timePart]
                        
    
    def getUserName(self, line):
        
        closingBracketIndex = line.find(']')
        colonIndex = line.find(':', closingBracketIndex)
        
        return line[closingBracketIndex + 1:colonIndex]
    
 
    def getMessage(self, line, userName):
        
        userNameIndex = line.find(userName)
        colonIndex = line.find(':', userNameIndex)
        return line[colonIndex + 1:]
        
    
    def convertToHtml(self, inputFileName):

        #open input file for reading
        self.inputFileHandle = open(inputFileName, 'r')
        
        # print details of input file
        print "Input file details: ", self.inputFileHandle
        
        # calculate output file name
        outputFileName = os.path.basename(inputFileName)
        (baseName, extension) = os.path.splitext(outputFileName)
        
        # open ouptut file for writing
        self.outputFileHandle = open(baseName + ".html", 'w')
        # print details of output file             
        print "Output file details: ", self.outputFileHandle
        
        #write html header
        self.writeHeader(baseName)
        
        # start reading and processing file line by line
        # typical format "[8/30/2013 12:34:57 PM] Abhishek  Bansal: copied"
        for line in self.inputFileHandle:
            self.outputFileHandle.write("<tr>")
            
            # if we fide a  openeing square bracket initially then its a new chat emtry from some User
            if line[0] == '[':
                timestamp = self.getTimeStamp(line)

                # now if timestamp is not none then try to find user who entered chat
                if timestamp is not None:
                    userName = self.getUserName(line)
                    
                    # add as a new user if name not already there in list
                    if userName and userName not in self.userList:
                        print "Adding " + userName + " to list"
                        self.userList.append(userName)
                    
                    #now we have timestamp and user name seperated out lets get the actual message now
                    message = self.getMessage(line, userName)
                    
                    #start writing data in table row
                    
                    # dont write user name if same user entered multiple chat entries
                    if (userName != self.prevUserName):
                        self.outputFileHandle.write("<td width = \"20%\">")
                        self.outputFileHandle.write("<div class=\"bubble date\">")
                        self.outputFileHandle.write(userName)
                        self.outputFileHandle.write("</div>")
                        self.outputFileHandle.write("</td>")
                        
                        self.prevUserName = userName
                        
                    else: #make a blank table data
                        self.outputFileHandle.write("<td width = \"200\">")
                        self.outputFileHandle.write("</td>")
                    
                    self.outputFileHandle.write("<td width = \"600\" style=\"word-wrap: break-word;\">")
                    self.outputFileHandle.write("<div class=\"bubble in\">")
                    self.outputFileHandle.write(message)
                    self.outputFileHandle.write("</div>")
                    self.outputFileHandle.write("</td>")
                    
                    self.outputFileHandle.write("<td width = \"200\">")
                    self.outputFileHandle.write("<div class=\"bubble date\">")
                    
                    # dont write date repeatedly write date only if it has changed
                    if self.prevDate is None or self.prevDate != timestamp[0]:
                        self.outputFileHandle.write("<b>")
                        self.outputFileHandle.write(timestamp[0])                        
                        self.outputFileHandle.write("</b>")
                        self.prevDate = timestamp[0]
                        self.outputFileHandle.write("&nbsp")
                    
                    self.outputFileHandle.write(timestamp[1])
                                                
                    self.outputFileHandle.write("</div>")
                    self.outputFileHandle.write("</td>")
                            
            else:
                # then its not a new chat line but continue writing it whatever it is in a chat bubble
                # make a blank table data                
                self.outputFileHandle.write("<td width = \"200\">")
                self.outputFileHandle.write("</td>")
                        
                # make a chat bubble
                self.outputFileHandle.write("<td width = \"600\" style=\"word-wrap: break-word;\">")
                self.outputFileHandle.write("<div class=\"bubble in\">")
                self.outputFileHandle.write(line)
                self.outputFileHandle.write("</div>")
                self.outputFileHandle.write("</td>")
                
                # make a blank table data                
                self.outputFileHandle.write("<td width = \"200\">")
                self.outputFileHandle.write("</td>")
                
            self.outputFileHandle.write('</tr>')
                
        self.inputFileHandle.close()
        self.outputFileHandle.close()
            

# program control starts from here

if __name__ == '__main__':
    
    skypeTextToHtml = SkypeTextToHtml()
    
    # give input file here
    skypeTextToHtml.convertToHtml('test.txt')