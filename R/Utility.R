
#Code complete
#Parse the input parameters from a file
parseParams <- function(n, fileName){
	conn <- file(fileName,open="r")
	linn <- readLines(conn)
	for(i in 0:n){
		kArray <- as.integer(unlist(strsplit(linn[n*i+1],",")))
		arrivals <- as.double(unlist(strsplit(linn[n*i+2],",")))
		omega <- as.double(linn[n*i+3])
		omega_0 <- as.double(linn[n*i+4])
		alpha <- as.double(linn[n*i+5])
		initials <- as.integer(unlist(strsplit(linn[n*i+6], ",")))
		testset <- as.double(unlist(strsplit(linn[n*i+7],",")))
		parameters[i] <- list(k=kArray, arvl = arrivals, omg = omega, omg_0 = omega_0, al = alpha, ini = initials, ts = testset)
	}
	close(conn)
	return parameters
}

# Code complete
# parse  the rank list after every time window
# format : ts te <listof,ranked,ids>()
# return the list of constraints and a total number of slack variables 
parseRank <- function(rankfileName){

	rankmatrix = {}
	conn <- file(rankfileName, open="r")
	linn <- readLines(conn)
	sc <- 0
	for(i in 0:length(linn)){
		argList <- (unlist(strsplit(linn[i]," ")))
		ts <- as.integer(argList[1])
		te <- as.integer(argList[2])
		idList <- as.integer(unlist(strsplit(argList[3], ",")))
		for (id_i in 1:length(idList)){
			for (id_j in id_i+1:length(idList)){
				rankmatrix[sc] = list(ts= ts, te=te, id1= id_i, id2=id_2,slackid = sc)
				sc <- sc + 1
			}
		}

	}
	return rankmatrix	
}

#Code complete #Code Checked
#The coefficient value of the lambda component in constraints gradient
calculate_coef_lambda <- function(epsilon, ts, te){
	return(-(exp(-epsilon*te) - exp(-epsilon*ts))/epsilon)
}

#Code complete #Code Checked
#The coefficient value of the beta component in constarinrs gradient
calculate_coef_beta <-function(omega, omega_0, k, arrivals, ts, te){
	first_term <- 0
	second_term <- 0
	return_value <- 0
	for(i in 1:length(arrivals)){
  		if(arrivals[i] < te ){
  			first_term <- ((1 /(omega_0 + (omega / k[i]))) * (exp( -(omega_0 + (omega / k[i])) * (te - 
  				arrivals[i]))))
  		}
  		if(arrivals[i] < ts ){
  			second_term <- ((1 /(omega_0 + (omega / k[i]))) * (exp( -(omega_0 + (omega / k[i])) * (ts - 
  				arrivals[i]))))	
  		}
  		return_value <- return_value - (first_term - second_term)/(omega_0 + omega/k[i])
  	}
  	return return_value
}

#Code Complete checked
#The gradient of likelihood function with respect to lambda
gradUtilityLambda <- function(omega, omega_0, k, arrivals, epsilon, lambda_0, beta){
	n <- length(arrivals)
	first_term <- (exp(-epsilon * arrivals[n]) - exp(-epsilon * arrivals[1])) / epsilon

  	Ai <- c(0,sapply(2:n, function(z) {
			sum(exp(-(omega_0 + omega/k[z]) * (arrivals[z] - arrivals[1:(z-1)])))
		}))	
	denom <- lambda_0 * exp(-epsilon*arrivals) + beta * Ai
  	second_term <- sum(exp(-epsilon*arrivals)/ denom)
  	return first_term + second_term
} 

#Code complete #Code checked
#The gradient of likelihood function with respect to beta
gradUtilityBeta <- function(omega, omega_0, k, arrivals, epsilon, lambda_0, beta){
	n <- length(arrivals)

	first_term <- 0
	for(i in 1:length(k)){
  	first_term <- first_term + (1 /(omega_0 + (omega / k[i]))) * (exp( -(omega_0 + (omega / k[i]))* 
  			(arrivals[n] - arrivals[i])))
  	}
	
	numerator <- c(0,sapply(2:n, function(z) {
			sum(exp(-(omega_0 + omega/k[z]) * (arrivals[z] - arrivals[1:(z-1)])))
	}))	
	
	denominator <- (lambda_0 * exp(-epsilon*arrivals) + beta * numerator)
	second_term <- sum(numerator / denominator)	
	
	return first_term + second_term
}

# Not required currently
gradUtilityLambdaConstraints <- function(w, w_0, k<array>, t<array>, epsilon){

}

#Not required currently
gradUtilityBetaConstraints <- function(w, w_0, k<array>, t<array>, epsilon){

}

# Not required currently
#creating constraints
createContraints <- function(ts, te, params_i, params_j){

	A <- (exp(-epsilon * te) - exp(-epsilon * ts))/(-epsilon)
	B <- 0
	C <- 0

	omega_i <- params_i[1]
	omega_0_i <- params_i[2]
	arrivals_i <- params_i[3]
	k_i <- params_i[4]

	omega_j <- params_j[1]
	omega_0_j <- params_j[2]
	arrivals_j <- params_j[3]
	k_j <- params_j[4]

	for(i in 1:length(k_i)){
  		if(arrivals_i[i] < te ){
  			B <- B + ((1 /(omega_0_i + (omega_i / k_i[i]))) * (exp( -(omega_0_i + (omega_i / k_i[i]))* (te - 
  				arrivals_i[i]))))
  		}
  		if(arrivals[i] < ts ){
  			C <- C + ((1 /(omega_0_i + (omega_i / k_i[i]))) * (exp( -(omega_0_i + (omega_i / k_i[i]))* (ts - 
  				arrivals_i[i]))))	
  		}
  	}


  	for(i in 1:length(k_i)){
  		if(arrivals_j[i] < te ){
  			B <- B + ((1 /(omega_0_j + (omega_j / k_j[i]))) * (exp( -(omega_0_j + (omega_j / k_j[i]))* (te - 
  				arrivals_j[i]))))
  		}
  		if(arrivals[i] < ts ){
  			C <- C + ((1 /(omega_0_j + (omega_j / k_j[i]))) * (exp( -(omega_0_j + (omega_j / k_j[i]))* (ts - 
  				arrivals_j[i]))))	
  		}
  	}
  	#TODO
}