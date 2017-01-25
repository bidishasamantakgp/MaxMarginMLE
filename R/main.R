#Main Block
library(R.matlab)

source('/home/bidisha/2017-hashtag-code/MaxMarginMLE/R/likelihood.R')
source('/home/bidisha/2017-hashtag-code/MaxMarginMLE/R/initializer.R')


myArgs <- commandArgs(trailingOnly = TRUE)
#Arrival File name
fileName <- myArgs[1]
#rankfilename
rankfileName <- myArgs[2]

parameters <- parseParams(fileName)
#rankconstraints <- parseRank(rankfileName)
rankList <-parseRank(rankfileName)
epsilon<-0.00001
sc <- length(rankList)

x0 <- c(parameters[["initials"]], rep(c(0.001),each=sc))
lb <- c(rep(c(0), each=parameters[["n"]] * 2 +sc))
ub <- c(rep(c(200),each=parameters[["n"]]*2),rep(c(10), each=sc))

n <- c(parameters[["n"]])
alphaList <- parameters[["alpha"]]
testsetlist <- parameters[["testset"]]
#omega_0List <- parameters[["omega_0"]]
#omegaList <- parameters[["omega"]]
arrivalsList <- parameters[["arrivals"]]
initialList <- myArgs[5]

parsedArgument <-parseArgument(initialList)
omega_0List <- parsedArgument[["omega_0"]]
omegaList <- parsedArgument[["omega"]]
kArrayList <- parameters[["k"]]



m<-eval_grad_constraints1( omega_0List, omegaList, kArrayList, arrivalsList, rankList, n, epsilon ) 
x0<-getinitials(m, 2*n, length(rankList))
print(x0)


# res0 <- nloptr( x0=x0 ,eval_f=loglikeModelSystem, eval_grad_f=eval_grad_objfnc,lb = lb,ub = ub,
#  	eval_g_ineq = eval_constraints, eval_jac_g_ineq = eval_grad_constraints, 
#  	opts = list("algorithm" = "NLOPT_LD_MMA", "print_level" = 2, "check_derivatives" = TRUE, 
#  	"check_derivatives_print" = "all","maxeval"=100),arrivalsList = parameters[["arrivals"]], 
#  	kArrayList = parameters[["k"]], omega_0List = omega_0List, omegaList = omegaList, epsilon = epsilon, 
#  	n = parameters[["n"]], rankList=rankList)

res0 <- nloptr( x0=x0 ,eval_f=loglikeModelSystem, lb = lb,ub = ub,eval_g_ineq = eval_constraints, 
	opts = list("algorithm" = "NLOPT_LN_COBYLA", "print_level" = 2),
	arrivalsList = parameters[["arrivals"]], kArrayList = parameters[["k"]], 
	omega_0List = omega_0List, omegaList = omegaList, epsilon = epsilon, n = parameters[["n"]], rankList=rankList)

print(res0)

solution <- res0$solution
print(solution)

#outputfile

writeFileName <- myArgs[4]

#hashtagnamefile
hashfile <- myArgs[3]
conn <- file(hashfile,open="r")
linn <- readLines(conn)

for (i in 1:n) {
	writeFileNameNew <- paste(c(writeFileName,linn[i],'.mat'),collapse='')
	writeMat(writeFileNameNew, alpha=alphaList[[i]], beta=solution[2*i], lambda_0=solution[2*i - 1], epsilon=epsilon, 
		omega_0=omega_0List[[i]], omega=omegaList[[i]], testSet=testsetlist[[i]], trainSize=length(arrivalsList[[i]]), 
		outputFile=writeFileName)
}
