
NameVal = "Tanh"

Plu_data <- read.delim(paste("Plu/ErrorAvrage", NameVal," copy.txt", sep = ""), header = FALSE)
Plu_Avg = list()


He_data <- read.delim(paste("He/ErrorAvrage", NameVal," copy.txt", sep = ""), header = FALSE)
He_Avg = list()


Nox_data <- read.delim(paste("Nox/ErrorAvrage", NameVal," copy.txt", sep = ""), header = FALSE)
Nox_Avg = list()


Ser_data <- read.delim(paste("Ser/ErrorAvrage", NameVal, " copy.txt", sep = ""), header = FALSE)
Ser_Avg = list()


Xav_data <- read.delim(paste("Xav/ErrorAvrage",NameVal," copy.txt", sep = ""), header = FALSE)
Xav_Avg = list()

for (i in 1:20)
{
	Ser_Avg  = append(Ser_Avg,as.double(Ser_data[i,1]))
	Nox_Avg = append(Nox_Avg,as.double(Nox_data[i,1]))
	He_Avg = append(He_Avg,as.double(He_data[i,1]))
	Plu_Avg = append(Plu_Avg,as.double(Plu_data[i,1]))
	Xav_Avg = append(Xav_Avg,as.double(Xav_data[i,1]))
}



Xav_Avg = as.numeric(Xav_Avg)
Ser_Avg = as.numeric(Ser_Avg)
Nox_Avg = as.numeric(Nox_Avg)
He_Avg = as.numeric(He_Avg)
Plu_Avg = as.numeric(Plu_Avg)





DataLis = c(He_Avg, Nox_Avg ,Plu_Avg, Ser_Avg, Xav_Avg)


Pvals = matrix(c(0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0), nrow = 5)


for (i in 1:5)
{
	for (j in 1:5)
	{
		if(i == j)
		{
			Pvals[i,j]= "  /  "
		}
		else
		{
		r = i -1
		c = j -1
		p = (c*20)+1
		d = (c*20)+20
		hhhgreg = DataLis[p:d]
		
		g = (r*20)+1
		h = (r*20)+20
		walmart = DataLis[g:h]
		print(i)
		print(j)
		MannU = wilcox.test(walmart, hhhgreg, alternative = "two.sided", paired = FALSE, exact = FALSE, correct = TRUE)
		CurrPval = signif(round(as.double(MannU[3]),3), 3)
		if(CurrPval == 0)
		{
			CurrPval <- "0.000"
		}
		Pvals[i,j]= CurrPval
		}
	}
}
rownames(Pvals) <- c("He ", "Nox", "Plu", "Ser", "Xav")
colnames(Pvals) <- c("    | He   ", "Nox  ", "Plu  ", "Ser  ", "Xav  ")
print(Pvals)
write.table(Pvals, file =paste("Tables-US1990/", NameVal,".txt", sep = ""), sep = "|")

