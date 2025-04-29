
from lxml import etree
import re
from datetime import datetime
import os
from pathlib import Path


def parse_failure_element(failure_element):
    """
    parses out Expected value and asserted value in failure report element, and
    returns it in a way that will fit in an adoc table fine

    Parses the message string in the failiure message.

    Args:
        failure_element (lxml.etree.Element): failure element in xml report typically an element will look like :literal:`<failure message="{Expected value: TRUE, Asserted value: FALSE}">"FAIL"</failure>`

    Returns:
        str: a string that will not break in an adoc table formatting

    """
    errorRegex = r'{Expected value: (.*), Asserted value: (.*)}'
    raw_failure_message = failure_element.get("message", "Unknown reason")
    match = re.match(errorRegex, raw_failure_message)
    if match:
        expected_value, asserted_value = match.groups()
        failure_message = f"Expected value: {expected_value} +\nAsserted value:  {asserted_value}"#the + symbol here before the newline is to make the adoc table formatting work
    else:
        failure_message = raw_failure_message
    
    return failure_message

def parse_xml_to_adoc(xml_file, output_adoc,write_header=True):
    """
    Parses an xml test report file from Caraya and writes the results to an adoc file

    Args:
        xml_file (str): path to the xml file to be parsed
        output_adoc (str): path to the adoc file to be written
    Returns:
        None - but writes the adoc file to the output path
    """
    tree = etree.parse(xml_file)
    root = tree.getroot()
    mainTestSuites = root.getchildren()
    timestamp = None#init timestamp to populate with first testsuite timestamp
    with open(output_adoc, "w",encoding="utf-8") as adoc:
        adoc.write("= Test Results Documentation\n\n")
        
        for testsuite in mainTestSuites:
            suite_name = testsuite.get("name")
            total_tests = testsuite.get("tests")
            errors = testsuite.get("errors")
            failures = testsuite.get("failures")
            test_timestamp = testsuite.get('timestamp')
            if not timestamp:
                timestamp = test_timestamp
            nPassedTests = int(total_tests) - int(errors) - int(failures)

            adoc.write(f"== {suite_name}\n\n")
            adoc.write(f"* Total Tests: {total_tests}\n\
                         * Passed Tests : {nPassedTests}\n")
            errors = testsuite.get('errors')
            if int(errors) !=0:
                adoc.write(f"* Errors : {errors}\n")
            failures = testsuite.get('failures')
            if int(failures) !=0:
                adoc.write(f"* Failures ‼: {failures}\n")

            adoc.write("|===\n| Test Name | Status | Failure Reason \n\n")
            
            for testcase in testsuite.findall("testcase"):
                test_name = testcase.get("name")
                failure = testcase.find("failure")
                skipped = testcase.find("skipped")
                
                if failure is not None:
                    status = "FAIL "
                    reason = parse_failure_element(failure)
                elif skipped is not None:
                    status = "SKIPPED "
                    reason = "Test was skipped"
                else:
                    status = "PASS "
                    reason = "-"
                
                adoc.write(f"| {test_name} | {status} | {reason} \n\n")
            
            adoc.write("|===\n\n")

        if not timestamp:
            timestamp = "1970-01-01T00:00:00"  # Default timestamp 
        # reformatting test timestamp to look more readable
        dt = datetime.fromisoformat(timestamp)
        readable_timestamp = dt.strftime("%A, %d %B %Y %I:%M:%S %p (UTC%z)")
        # writing general information for the test to the end of the file
        adoc.write(f"Tests performed using framework: {root.get('framework-name','not specified')} \
                   V:{root.get('framework-version','unknown')}\n\
                   Test run on: {readable_timestamp}\n\n")
    
    print(f"Documentation written to {output_adoc}")


def parse_multiple_to_adoc(dict_of_xmls,outputfile,temp_XML_Folder):
    """
    parses a list of dictionarys of xml filepaths to one cohesive Adoc output

    list of dictionaries should look like:
    [{'test_name':<name>,'xml_filepath':<filepath_to_xml>},
    {'test_name':<name>,'xml_filepath':<filepath_to_xml>},...]

    where filepath_to_xml can be a string of pathlib.Path object
    """
    #temp_XML_Folder = Path(temp_XML_Folder)
    filemode = 'w+'
    for iXML in dict_of_xmls:
        output_ADoc = temp_XML_Folder.joinpath(f"{iXML['test_name']}.adoc")
        
        parse_xml_to_adoc(iXML['xml_filepath'],output_ADoc,write_header=filemode=="w+")
        #read contents of adoc and dump into output file
        with open(output_ADoc,'r') as adocfile:
            adocContents = adocfile.read()
        
        #write to output file
        with open(outputfile,filemode) as f:
            f.write(adocContents)
        if filemode == 'w+':
            filemode = 'a'#change to append after first file

    

if __name__ == "__main__":
    """
    runs test on example files
    """
    baseDir = os.path.join("..","Tests","exampleFiles")
    baseDir = os.path.abspath(baseDir)
    TEST_REPORT_XML = os.path.join(baseDir,"exampleTestXml.xml")
    CONVERTED_ADOC_FILEPATH = os.path.join(baseDir,"exampleTestAdoc.adoc")
    
    parse_xml_to_adoc(TEST_REPORT_XML,CONVERTED_ADOC_FILEPATH)
    
