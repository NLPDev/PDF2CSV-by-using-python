import PyPDF2
import csv
import sys
import glob
import errno

path = './input/*.pdf'
files = glob.glob(path)
for name in files: # 'file' is a builtin type, 'name' is a less-ambiguous variable name.

    with open(name) as pdf_file: # No need to specify 'r': this is the default.

		ll = len(pdf_file.name)
		oot = pdf_file.name[8:ll - 4]

		oot = './output/' + oot + '.csv'
		read_pdf = PyPDF2.PdfFileReader(pdf_file)
		number_of_pages = read_pdf.getNumPages()
		page = read_pdf.getPage(0)
		i = 0

		# print (number_of_pages)
		with open(oot, 'wb') as f:

			fieldnames = ['Rep#', 'Brand', 'Customer Number', 'Customer Name', 'Order Number', 'Order Date',
						  'Invoice Number', 'Invoice Date', 'Invoice Line', 'Invoice Amount', 'Item Number',
						  'Comission %', 'Comission Amount', 'Product Type', 'Discount']
			#writer = csv.DictWriter(f, fieldnames=fieldnames)
			writer=csv.writer(f)
			writer.writerow(fieldnames)


			while i < number_of_pages:
				page = read_pdf.getPage(i)
				page_content = page.extractText()

				i = i + 1
				st=""
				st=st+page_content
				res=st.split()
				flag=0
				j=2
				field_len=len(fieldnames)
				if i==1 :
					for k in range(field_len):
						fieldnames[k] = ''

				kk=0
				brand=''
				rep=''
				aa=['','','']
				for element in res:
					if kk==1:
						brand=element
					if kk==10:
						rep=element[len(element)-5:len(element)]


					kk = kk + 1
					if flag==11:
						if element[0]=='C':
							cnt_c=0
							flag=5
							continue
						else:
							flag=1

					if flag==5:
						if cnt_c==3:
							flag=1
							j=2
							for k in range(field_len):
								fieldnames[k] = ''
							fieldnames[3]='Customer Totals'
							fieldnames[9]=aa[1]
							fieldnames[12]=aa[2][0:len(aa[2])-5]
							#writer.writerow(fieldnames)
							for k in range(field_len):
								fieldnames[k] = ''
							fieldnames[2]=aa[2][len(aa[2])-5:len(aa[2])]
							fieldnames[3]=element
							j=3

							continue
						aa[cnt_c] = element
						cnt_c = cnt_c + 1
						continue



					if len(element)>3 and element[0:3]=='Dis':
						flag=1
						if len(element)>8:
							element=element[8:len(element)]
						else:
							continue

					if flag==0:
						continue

					if j==5 and element[0]=='H':
						j=6
						fieldnames[j]=element
						fieldnames[j-1]=''
						j=j+1
						continue

					if j==2 and element[1]=='4':

						fieldnames[4]=element
						j = 5
						continue


					if j==3 :

						if len(element)>1 and element[1]=='4':
							j=4
							fieldnames[j] = element
							j=j+1
							continue
						else:
							fieldnames[3]=fieldnames[3]+' '+element
							continue

					if flag==10:
						flag=1
						if element[len(element)-3]=='.':
							fieldnames[14]=element
							fieldnames[1] = brand
							fieldnames[0] = rep
							writer.writerow(fieldnames)
							for k in range(field_len-4):
								fieldnames[k+4] = ''
							j=2
							flag=11
							continue
						else:
							fieldnames[14] = ''
							fieldnames[1] = brand
							fieldnames[0] = rep
							writer.writerow(fieldnames)
							for k in range(field_len-4):
								fieldnames[k+4] = ''
							if element[0]=='C':
								flag=5
								cnt_c=0
								continue
							j=2
							if element[0]=='0':
								j=4
								fieldnames[2]=''
								fieldnames[3]=''


					if element=='H' or element=='W':
						flag=10
						fieldnames[j]=element
						j=j+1
						continue

					if flag==1:
						if j==field_len:
							fieldnames[1]=brand
							fieldnames[0]=rep
							writer.writerow(fieldnames)
							for k in range(field_len-4):
								fieldnames[k+4] = ''
							j=2
						fieldnames[j]=element
						j=j+1



