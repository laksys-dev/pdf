#pip install pdfplumber
import pdfplumber
import os, os.path
import re

filenames = [f for f in next(os.walk('.'))[2] if f.endswith('pdf')]
csvfile_exists = False

if len(filenames) == 0:
	print("No pdf files found in current folder exiting...")
else:
	csvfile = "out.csv"

	header = ['Year', 'Period', 
		'GSTIN', 'Legal Name', 'Trade Name', 'ARN', 'Date of ARN',
		'Total Taxable Value', 'Integrated Tax', 'Central Tax', 'State/UT Tax', 'Cess',
		'Tax paid in cash - Integrated tax', 'Tax paid in cash - Central tax', 'Tax paid in cash - State UT tax', 'Tax paid in cash - Cess', 'Source file']

	if os.path.isfile(csvfile):
		csvfile_exists = True	

	csv = open(csvfile, "a")	

	if not csvfile_exists:
		for head in header:
			csv.write(head)
			csv.write(",")
		csv.write("\n")

	def ext(str):
		return re.findall('[0-9.]+', str)[0]

	for file in filenames:
		try:
			pdf  = pdfplumber.open(file)

			page1 = pdf.pages[0]
			tables = page1.find_tables()

			t0 = tables[0].extract(x_tolerance = 5)
			year   = t0[0][1]
			period = t0[1][1]			

			t1 = tables[1].extract(x_tolerance = 5)
			gstin       = t1[0][1]
			legal_name  = t1[1][1] 
			trade_name  = t1[2][1]
			arn         = t1[3][1]
			date_of_arn = t1[4][1]			

			t2 = tables[2].extract(x_tolerance = 5)
			total_taxable_value = ext(t2[1][1])
			integrated_tax      = ext(t2[1][2])
			central_tax 	    = ext(t2[1][3])
			state_ut_tax 	    = ext(t2[1][4])
			cess 		   		= ext(t2[1][5])		

			page2  = pdf.pages[1]
			tables = page2.find_tables()

			t3 = tables[2].extract(x_tolerance = 5)
			if t3[0][0] != 'Description':
				t3 = tables[3].extract(x_tolerance = 5)
			tax_paid_in_cash_integrated_tax = ext(t3[3][6])
			tax_paid_in_cash_central_tax    = ext(t3[4][6])
			tax_paid_in_cash_state_ut_tax   = ext(t3[5][6])
			tax_paid_in_cash_cess 		    = ext(t3[6][6])

			csv.write(year)
			csv.write(",")
			csv.write(period)
			csv.write(",")

			csv.write(gstin)
			csv.write(",")
			csv.write(legal_name)
			csv.write(",")
			csv.write(trade_name)
			csv.write(",")
			csv.write(arn)
			csv.write(",")
			csv.write(date_of_arn)
			csv.write(",")

			csv.write(total_taxable_value)
			csv.write(",")
			csv.write(integrated_tax)
			csv.write(",")
			csv.write(central_tax)
			csv.write(",")
			csv.write(state_ut_tax)
			csv.write(",")
			csv.write(cess)
			csv.write(",")

			csv.write(tax_paid_in_cash_integrated_tax)
			csv.write(",")
			csv.write(tax_paid_in_cash_central_tax)
			csv.write(",")
			csv.write(tax_paid_in_cash_state_ut_tax)
			csv.write(",")
			csv.write(tax_paid_in_cash_cess)
			csv.write(",")
			csv.write(file)

			csv.write('\n')
			print ( file + " extracted successfully!")
		except:
			print("Something went wrong on file: " + file)
			continue
	csv.close()

