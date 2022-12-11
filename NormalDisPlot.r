plotx <- seq(-2, 2, by = 1)
ploty <- seq(0, 3, by = 0.75)
for (i in 1:100)
{

		png(file = paste("NormalDisPicts/dnm", i, ".png", sep = ""))
		plot(plotx, ploty, col = "white", xlab = "x", ylab = "Density of G(0, f(i))", main = paste("i =", i))
		curve(dnorm(x, mean = 0, sd = ((i+20)^(4/(i+20)) -1)), add = TRUE, col = "red")
		curve(dnorm(x, mean = 0, sd = (sqrt(2/i))), add = TRUE, col = "blue")
		dev.off()
}



#Red is Self-Root
#Blue is He