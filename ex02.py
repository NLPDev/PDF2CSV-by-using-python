import PyPDF2
import csv
import sys
import glob
import errno

path = './input/*.pdf'
files = glob.glob(path)
for name in files:  # 'file' is a builtin type, 'name' is a less-ambiguous variable name.

	with open(name) as pdf_file:  # No need to specify 'r': this is the default.

		ll = len(pdf_file.name)
		oot = pdf_file.name[8:ll - 4]

		oot = './output/' + oot + '.csv'
		read_pdf = PyPDF2.PdfFileReader(pdf_file)
		number_of_pages = read_pdf.getNumPages()
		page = read_pdf.getPage(0)
		i = 0

		# print (number_of_pages)
		with open(oot, 'wb') as f:

			fieldnames = ['Rep#', 'Brand', 'Customer Number', 'Customer Name', 'Invoice Number', 'Invoice Date', 'Item Group', 'Qty', 'Invoice Amount', 'Item Number',
						  '%', 'Amount Due']
			# writer = csv.DictWriter(f, fieldnames=fieldnames)
			writer = csv.writer(f)
			writer.writerow(fieldnames)

			while i < number_of_pages:
				page = read_pdf.getPage(i)
				page_content = page.extractText()

				i = i + 1
				st = ""
				st = st + page_content
				res = st.split()
				flag = 0
				j = 2
				field_len = len(fieldnames)
				for k in range(field_len):
					fieldnames[k] = ''
				kk = 0
				brand = ''
				aa = ['', '', '','','','','','','']
				cnt_i=0
				for element in res:

					if kk==1:
						brand=element
					kk=kk+1

					if len(element)>3 and element[0:3]=="Due":
						flag=1
						fieldnames[j]=element[3:8]
						j=j+1
						continue

					if flag==0:
						continue

					if flag==5:
						if cnt_i==7:
							for k in range(12):
								fieldnames[k]=''
							fieldnames[3]='Item Group Totals'
							fieldnames[5]=aa[3]
							fieldnames[8]=aa[4]
							fieldnames[10]=aa[5]
							if len(aa[6])>7:
								fieldnames[11] = aa[6][0:len(aa[6]) - 5]
							else:
								fieldnames[11]=aa[6]

							writer.writerow(fieldnames)
							for k in range(12):
								fieldnames[k]=''
							fieldnames[2]=aa[6][len(aa[6])-5:len(aa[6])]
							fieldnames[3]=element
							j=3
							flag=1
							continue

						aa[cnt_i]=element

						cnt_i=cnt_i+1
						continue


					if j==3:
						if element[0]=='V':
							fieldnames[j+1]=element
							j=j+2
							continue
						if element[0]=='M' and element[1].isdigit():
							fieldnames[j + 1] = element
							j = j + 2
							continue
						fieldnames[j]=fieldnames[j]+' '+element
						continue

					if j==11:
						if len(element)>7:
							fieldnames[j]=element[0:len(element)-5]
							writer.writerow(fieldnames)
							for k in range(12):
								fieldnames[k]=''
							fieldnames[2]=element[len(element)-5:len(element)]
							j=3
							continue

						else:
							fieldnames[j] = element
							writer.writerow(fieldnames)
							for k in range(12):
								fieldnames[k] = ''
							flag=5
							cnt_i=0
						j=2
						continue

					fieldnames[j]=element
					j=j+1




