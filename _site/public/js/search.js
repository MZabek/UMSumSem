// Based on a script by Kathie Decora : katydecorah.com/code/lunr-and-jekyll/

//Create the lunr index for the search

var index = elasticlunr(function () {
  this.addField('title')
  this.addField('author')
  this.addField('layout')
  this.addField('content')
  this.setRef('id')
});

//Add to this index the proper metadata from the Jekyll content



index.addDoc({
  title: "Basel III Capital Requirements and Bank Credit Supply",
  author: null,
  layout: "post",
  content: "May 30 (Slot 1) - Owen Nie\n\nLocation: Lorch 301\n\nThis paper studies the effect of the implementation of Basel III global bank-\ning regulatory rules on bank credit supply. I exploit cross-country differences in\nthe implementation schedule of Basel III rules and focus on capital requirement,\nthe rest and only Basel III rule already in force. Contrary to what relevant\ntheory would predict, the treatment effect of higher equity requirement in this\nsample is an increase of aggregate credit supply of 5.6 percent on average. The\neffects are identified only when announcement is used as measure of treatment,\nnot with publication of draft regulations or formal dates of implementation.\n\n",
  id: 0
});
index.addDoc({
  title: "Domestic Misallocation from 'Profit-shifting' FDI with Heterogeneous Firms",
  author: null,
  layout: "post",
  content: "June 08 (Slot 1) - Will Boning\n\nLocation: Lorch 301\n\nWhen corporate taxation leads firms to reduce their output, selection by large, profitable firms into FDI for purely profit-shifting motives lowers shifting firms’ tax-inclusive marginal costs. In general equilibrium with CES preferences as in Melitz (2003), if some firms do not shift profits, profit-shifting results in heterogeneous markups over real marginal cost, distorting the allocation of inputs from non-shifting to shifting firms. If the marginal producing firm does not shift, then profit-shifting raises the productivity threshold for production excessively, reducing variety and welfare. Heterogeneous, as opposed to homogeneous, profit-shifting has general equilibrium welfare effects.\n\n",
  id: 1
});
index.addDoc({
  title: "Ensuring Against Trade Shocks",
  author: null,
  layout: "post",
  content: "June 08 (Slot 2) - Benjamin Glass\n\nLocation: Lorch 301\n\nI describe a two-period general equilibrium model.  Agents buy and sell forward contracts in the first period.  The second period has an open economy state and a closed economy state.   If agents are risk-averse and all markets are both complete &amp; undistorted, then all agents must weakly prefer that the open economy state obtain than that the closed economy state obtain.  Thus, there are no losers from trade.\n\n",
  id: 2
});
index.addDoc({
  title: "The Economic Consequences of Immigrant Disenfranchisement",
  author: null,
  layout: "post",
  content: "June 13 - Morgan Henderson\n\nLocation: Lorch 301\n\nFrom 1864 to 1926, twenty-three states and territories disenfranchised non-citizen immigrants, which represented a significant shock to electorates at the time. I estimate the effects of this disenfranchisement on voting outcomes, public spending, and crime. I find that it resulted in an immediate and sustained drop in mayoral and gubernatorial vote totals, with large effect sizes relative to the magnitude of the disenfranchised population. Consistent with findings from political science, the largest reductions in vote totals were concentrated in the politically uncompetitive states. I find little evidence that disenfranchisement affected partisan vote shares. States significantly reduced their spending, both in aggregate and as a share of the budget, directed toward education and social services, and there is suggestive evidence that cities significantly reduced their spending on water services. Consistent with a model of local political vote maximization with imperfect screening, I document a substantial reduction in the likelihood of a disenfranchised immigrant obtaining public employment. Finally, I present suggestive evidence that disenfranchisement led to a temporary increase in homicide rates.\n\n",
  id: 3
});
index.addDoc({
  title: "Short-Term Disability Insurance, Maternity Leave, and the Rise of Working Mothers",
  author: null,
  layout: "post",
  content: "June 17 (Slot 1) - Brenden Timpe\n\nLocation: Lorch 301\n\n",
  id: 4
});
index.addDoc({
  title: "The Demand Side of Structural Productivity Estimation",
  author: null,
  layout: "post",
  content: "June 20 - Andrew Usher\n\nJoint work with: Alberto Arredondo\n\nLocation: Lorch 301\n\n",
  id: 5
});
index.addDoc({
  title: "Consumer behavior in crowdfunding markets",
  author: null,
  layout: "post",
  content: "June 22 - Evan Wright\n\nLocation: Lorch 301\n\nReward-based crowdfunding provides an alternative, relatively low risk way for entrepreneurs and small businesses to raise capital. We provide an empirical analysis of consumer dynamics, finding that consumers are more likely to pledge to a crowdfunding project the closer a project is to its goal, consistent with previous literature; the resulting effect is stronger for projects with large (&gt;$100k) goals than for small ones. Additionally, we introduce a dynamic theoretical model based on individual consumer choice which implies this real world behavior under certain distributional assumptions.\n\n",
  id: 6
});
index.addDoc({
  title: "Gender gaps in STEM career choices- The effect of information and encouragement among students in Colombia",
  author: null,
  layout: "post",
  content: "June 24 - Molly Hawkins\n\nJoint work with: Catalina Franco\n\nLocation: Lorch 301\n\nWomen participate in STEM careers at lower rates than men in many countries.\nThis situation represents a waste of creative intellectual resources and a potential shortfall of talent. STEM fields generally require more math and are more competitive to enter than other fields. However, men and women do not differ in terms of their innate cognitive abilities (OECD, 2015); so, all else equal, the observed differences in career choices across men and women remain a mystery. To contribute to our understanding of the gender gap in STEM, we conduct a pilot experiment in Colombia to provide evidence on two factors that may affect women’s career choices. Specifically, we address the questions of whether and to what extent providing information about minimum scores in a college admissions test and encouragement to do STEM can induce girls to choose STEM majors and careers. The results from the pilot indicate that women in the treatment are more likely to choose a STEM major as a second choice and are more accurate in the scores they report as required to pass the admissions test.\n\n",
  id: 7
});
index.addDoc({
  title: "Housing Investment and Cash-out Refinance",
  author: null,
  layout: "post",
  content: "June 27 (Slot 1) - Xiaoqing Zhou\n\nLocation: Lorch 301\n\n",
  id: 8
});
index.addDoc({
  title: "Aristos Hudson",
  author: null,
  layout: "post",
  content: "July 06 - Aristos Hudson\n\nLocation: Lorch 301\n\n",
  id: 9
});
index.addDoc({
  title: "Market Organization and Productive Efficiency- Evidence from the Texas Electricity Market",
  author: null,
  layout: "post",
  content: "July 11 - Yiyuan Zhang\n\nLocation: Lorch 301\n\n",
  id: 10
});
index.addDoc({
  title: "The Fiscal Consequences of Deunionization",
  author: null,
  layout: "post",
  content: "July 13 - Andrew Litten\n\nLocation: Lorch 301\n\n",
  id: 11
});
index.addDoc({
  title: "Retail Price Discrimination under Double Marginalization- A Welfare Analysis",
  author: null,
  layout: "post",
  content: "July 15 - Adam Dearing\n\nLocation: Lorch 301\n\n",
  id: 12
});
index.addDoc({
  title: "Presentation TBD",
  author: null,
  layout: "post",
  content: "July 20 (Slot 1) - Max Risch\n\nLocation: Lorch 201\n\nNote the change in location!\n\n",
  id: 13
});
index.addDoc({
  title: "Spatial Variation in Product Exit over the Business Cycle",
  author: null,
  layout: "post",
  content: "July 20 (Slot 2) - Laurien Gilbert\n\nLocation: Lorch 201\n\nNote the change in location!\n\n",
  id: 14
});
index.addDoc({
  title: "Michael Gelman",
  author: null,
  layout: "post",
  content: "July 22 - Michael Gelman\n\nLocation: Lorch 201\n\nNote the change in location!\n\n",
  id: 15
});
index.addDoc({
  title: "The IT Boom and other Unintended Consequences of the American Dream",
  author: null,
  layout: "post",
  content: "July 25 - Nicolas Morales-Gaurav Khanna\n\nLocation: Lorch 301\n\nWe use a general equilibrium model to study how the US internet boom and concurrent immigration policies led to a tech boom in India. Specically, we test the hypothesis that Indian students enrolled in engineering schools to gain employment in the rapidly growing US IT industry via the H-1B visa program. Those who could not join the US workforce remained in India, enabling the growth of an IT sector. Those who returned with acquired human capital and technology after the expiration of their H-1Bs, also contributed to the growing tech-workforce in India. The increase in IT sector productivity allowed India to eventually surpass the US in IT exports. The paper develops a general quilibrium\nmodel of firm-hiring, and of worker decisions to study and choose occupations in both the US and India supported by a rich descriptive analysis of the changes in the 1990s and early 2000s. We calibrate this model and perform counterfactual exercises to study the impact of immigration policies on the growth of these sectors in both countries. We find that the H-1B program induced Indians to switch to computer science (CS) occupations, increasing the non-migrant CS workforce in India by 4.9% in 2010. It also induced US workers to switch to non-CS occupations, reducing the US native CS workforce by 7%. Indian IT output is higher by 1.8%, India’s share in world IT production greater by 8.9%, and the combined income of both countries is higher by 1.5% under the H-1B program\n\n",
  id: 16
});
index.addDoc({
  title: "Are Devaluations Expansionary?",
  author: null,
  layout: "post",
  content: "July 27 - Christian Proebsting\n\nLocation: Lorch 301\n\n",
  id: 17
});
index.addDoc({
  title: "Measuring College Investment with Course-Taking",
  author: null,
  layout: "post",
  content: "July 29 - Julian Hsu\n\nLocation: Lorch 301\n\nWill provide when you guys need it for the announcement e-mail!\n\n",
  id: 18
});
index.addDoc({
  title: "The effect of a permanent change in income on economic decision making",
  author: null,
  layout: "post",
  content: "August 01 - Catalina Franco\n\nJoint work with: Meera Mahadevan\n\nLocation: Lorch 301\n\nThis project seeks to contribute to the literature studying the causal effect of poverty on economic decision-making. Previous studies have found evidence that when individuals are poor, they are more present-biased and their performance in a cognitive test is worse than when their liquidity constraint is alleviated. These results emerge from analyzing short-term variations in income but so far, there is no evidence of how permanent changes in income affect economic decision-making. We propose a design in which the permanent change in flow income is given by the transition from college to the labor market. By following students, who range from lower to higher income backgrounds, about to graduate in a university in Colombia, we are able to assess whether economic decision-making changes along the transition from college to the labor market.\n\n",
  id: 19
});
index.addDoc({
  title: "Tax Incidence with Heterogeneous Firm Evasion- Evidence from Airbnb Remittance Agreements",
  author: null,
  layout: "post",
  content: "August 03 - Eleanor Wilking\n\nLocation: Lorch 301\n\n",
  id: 20
});
index.addDoc({
  title: "Population growth, decline, and shocks to local labor markets",
  author: null,
  layout: "post",
  content: "August 05 - Mike Zabek\n\nLocation: Lorch 301\n\nI analyze the implications of people’s ties to their birth places. These strong attachments lead people to stay in declining areas and lead to large differences in the share of residents born in the places where they reside. I develop an otherwise standard Rosen (1979) and Roback (1982) model of spatial equilibrium to match these facts and derive further implications. The model implies that areas will have different migration elasticities depending on whether they have been growing or declining. The reason is that declining areas attract residents that were mostly born locally, and these residents are more inelastic. Since migration tends to equalize real wages across space, one implication is that real wages can decrease by more in declining areas. Another implication is that place based policies designed to address these differences will lead to smaller distortions in declining areas. I find independent support for these differences in migration elasticities using reduced form regressions with plausibly exogenous local labor demand shifters.\n\n",
  id: 21
});
index.addDoc({
  title: "Local Institutions, Public Goods Provision and the Process of Urbanization",
  author: null,
  layout: "post",
  content: "August 08 - Aakash Mohpal\n\nLocation: Lorch 301\n\n",
  id: 22
});
index.addDoc({
  title: "The regular and list prices- an empirical study of their response to demand shocks",
  author: null,
  layout: "post",
  content: "August 10 - Alberto Arredondo\n\nJoint work with: Andrew Usher\n\nLocation: Lorch 301\n\n",
  id: 23
});
index.addDoc({
  title: "The Causes and Consequences of Teacher Turnover",
  author: null,
  layout: "post",
  content: "August 12 - Daniel Hubbard\n\nJoint work with: Kolby Gadd, Brian Jacob\n\nLocation: Lorch 301\n\nPrevious research has established that students learn best from teachers with at least a few years of experience, and that teacher quality is often distributed inequitably in a way that further disadvantages students of color and lower-income students. We use administrative data from Michigan’s public school system to determine which factors are associated with teachers leaving their first jobs, and to look at where they go if they choose to change jobs. We find that teachers are more likely to leave when they teach more black students or more low-income students; teachers are less likely to leave if they attended college in Michigan or have master’s degrees. Turnover patterns over the business cycle are also fascinating; teachers hired during a recession are less likely to leave, even as the labor market improves during their tenure, indicating that districts may be able to screen candidates effectively when the applicant pool is large.\n\n",
  id: 24
});
index.addDoc({
  title: "The Price Elasticity of Demand and Monetary Policy Transmission",
  author: null,
  layout: "post",
  content: "August 15 - DongIk Kang\n\nLocation: Lorch 301\n\n",
  id: 25
});
index.addDoc({
  title: "Image Motivation and the Willingness to Pay for Health Products",
  author: null,
  layout: "post",
  content: "August 17 - Salma Khalid\n\nLocation: Lorch 301\n\n",
  id: 26
});
index.addDoc({
  title: "Consumer behavior in crowdfunding markets",
  author: null,
  layout: "post",
  content: "August 19 - Evan Wright\n\nLocation: Lorch 301\n\n",
  id: 27
});
index.addDoc({
  title: "Understanding the role of employers in high skilled immigration",
  author: null,
  layout: "post",
  content: "August 22 - Nicolas Morales\n\nLocation: Lorch 301\n\n",
  id: 28
});
index.addDoc({
  title: "Selection into migration and return migration",
  author: null,
  layout: "post",
  content: "August 24 - Alexander Persaud\n\nLocation: Lorch 301\n\n",
  id: 29
});
index.addDoc({
  title: "Labor Supply Decisions and Pensions- Evidence from Brazil",
  author: null,
  layout: "post",
  content: "August 26 - Ben Thompson\n\nLocation: Lorch 301\n\n",
  id: 30
});
index.addDoc({
  title: "Social security and family ties- a positive theory",
  author: null,
  layout: "post",
  content: "August 29 - Giacomo Brusco\n\nLocation: Lorch 301\n\nIn this paper I present a model in which both family ties and social security policy are endogenously determined. My model shows how family values interact with policy preferences, resulting in the prediction that countries with strong family ties tend to have more generous social security systems. I supplement my theoretical work with empirical evidence at the country level, showing that countries with stronger family ties are associated with higher public spending on pensions, and at the individual level, showing that stronger family ties are associated with stronger support for social security spending in the U.S.\n\n",
  id: 31
});
index.addDoc({
  title: "The Rise of Working Mothers and the 1975 Earned Income Tax Credit",
  author: null,
  layout: "post",
  content: "August 31 - Jacob Bastian\n\nLocation: Lorch 301\n\n",
  id: 32
});
index.addDoc({
  title: "Feiya shao",
  author: null,
  layout: "post",
  content: "September 05 - Feiya shao\n\nLocation: Lorch 301\n\n",
  id: 33
});
index.addDoc({
  title: "The effect of electricity price changes in the presence of capital adjustment costs",
  author: null,
  layout: "post",
  content: "September 07 - Sarah Johnston\n\nLocation: Lorch 301\n\n",
  id: 34
});
console.log( jQuery.type(index) );

// Builds reference data (maybe not necessary for us, to check)


var store = [{
  "title": "Basel III Capital Requirements and Bank Credit Supply",
  "author": null,
  "layout": "post",
  "link": "/texts/0001/",
}
,{
  "title": "Domestic Misallocation from 'Profit-shifting' FDI with Heterogeneous Firms",
  "author": null,
  "layout": "post",
  "link": "/texts/0002/",
}
,{
  "title": "Ensuring Against Trade Shocks",
  "author": null,
  "layout": "post",
  "link": "/texts/0003/",
}
,{
  "title": "The Economic Consequences of Immigrant Disenfranchisement",
  "author": null,
  "layout": "post",
  "link": "/texts/0004/",
}
,{
  "title": "Short-Term Disability Insurance, Maternity Leave, and the Rise of Working Mothers",
  "author": null,
  "layout": "post",
  "link": "/texts/0005/",
}
,{
  "title": "The Demand Side of Structural Productivity Estimation",
  "author": null,
  "layout": "post",
  "link": "/texts/0006/",
}
,{
  "title": "Consumer behavior in crowdfunding markets",
  "author": null,
  "layout": "post",
  "link": "/texts/0007/",
}
,{
  "title": "Gender gaps in STEM career choices- The effect of information and encouragement among students in Colombia",
  "author": null,
  "layout": "post",
  "link": "/texts/0008/",
}
,{
  "title": "Housing Investment and Cash-out Refinance",
  "author": null,
  "layout": "post",
  "link": "/texts/0009/",
}
,{
  "title": "Aristos Hudson",
  "author": null,
  "layout": "post",
  "link": "/texts/0010/",
}
,{
  "title": "Market Organization and Productive Efficiency- Evidence from the Texas Electricity Market",
  "author": null,
  "layout": "post",
  "link": "/texts/0011/",
}
,{
  "title": "The Fiscal Consequences of Deunionization",
  "author": null,
  "layout": "post",
  "link": "/texts/0012/",
}
,{
  "title": "Retail Price Discrimination under Double Marginalization- A Welfare Analysis",
  "author": null,
  "layout": "post",
  "link": "/texts/0013/",
}
,{
  "title": "Presentation TBD",
  "author": null,
  "layout": "post",
  "link": "/texts/0014/",
}
,{
  "title": "Spatial Variation in Product Exit over the Business Cycle",
  "author": null,
  "layout": "post",
  "link": "/texts/0015/",
}
,{
  "title": "Michael Gelman",
  "author": null,
  "layout": "post",
  "link": "/texts/0016/",
}
,{
  "title": "The IT Boom and other Unintended Consequences of the American Dream",
  "author": null,
  "layout": "post",
  "link": "/texts/0017/",
}
,{
  "title": "Are Devaluations Expansionary?",
  "author": null,
  "layout": "post",
  "link": "/texts/0018/",
}
,{
  "title": "Measuring College Investment with Course-Taking",
  "author": null,
  "layout": "post",
  "link": "/texts/0019/",
}
,{
  "title": "The effect of a permanent change in income on economic decision making",
  "author": null,
  "layout": "post",
  "link": "/texts/0020/",
}
,{
  "title": "Tax Incidence with Heterogeneous Firm Evasion- Evidence from Airbnb Remittance Agreements",
  "author": null,
  "layout": "post",
  "link": "/texts/0021/",
}
,{
  "title": "Population growth, decline, and shocks to local labor markets",
  "author": null,
  "layout": "post",
  "link": "/texts/0022/",
}
,{
  "title": "Local Institutions, Public Goods Provision and the Process of Urbanization",
  "author": null,
  "layout": "post",
  "link": "/texts/0023/",
}
,{
  "title": "The regular and list prices- an empirical study of their response to demand shocks",
  "author": null,
  "layout": "post",
  "link": "/texts/0024/",
}
,{
  "title": "The Causes and Consequences of Teacher Turnover",
  "author": null,
  "layout": "post",
  "link": "/texts/0025/",
}
,{
  "title": "The Price Elasticity of Demand and Monetary Policy Transmission",
  "author": null,
  "layout": "post",
  "link": "/texts/0026/",
}
,{
  "title": "Image Motivation and the Willingness to Pay for Health Products",
  "author": null,
  "layout": "post",
  "link": "/texts/0027/",
}
,{
  "title": "Consumer behavior in crowdfunding markets",
  "author": null,
  "layout": "post",
  "link": "/texts/0028/",
}
,{
  "title": "Understanding the role of employers in high skilled immigration",
  "author": null,
  "layout": "post",
  "link": "/texts/0029/",
}
,{
  "title": "Selection into migration and return migration",
  "author": null,
  "layout": "post",
  "link": "/texts/0030/",
}
,{
  "title": "Labor Supply Decisions and Pensions- Evidence from Brazil",
  "author": null,
  "layout": "post",
  "link": "/texts/0031/",
}
,{
  "title": "Social security and family ties- a positive theory",
  "author": null,
  "layout": "post",
  "link": "/texts/0032/",
}
,{
  "title": "The Rise of Working Mothers and the 1975 Earned Income Tax Credit",
  "author": null,
  "layout": "post",
  "link": "/texts/0033/",
}
,{
  "title": "Feiya shao",
  "author": null,
  "layout": "post",
  "link": "/texts/0034/",
}
,{
  "title": "The effect of electricity price changes in the presence of capital adjustment costs",
  "author": null,
  "layout": "post",
  "link": "/texts/0035/",
}
]

//Query

var qd = {}; //Gets values from the URL
location.search.substr(1).split("&").forEach(function(item) {
    var s = item.split("="),
        k = s[0],
        v = s[1] && decodeURIComponent(s[1]);
    (k in qd) ? qd[k].push(v) : qd[k] = [v]
});

function doSearch() {
  var resultdiv = $('#results');
  var query = $('input#search').val();

  //The search is then launched on the index built with Lunr
  var result = index.search(query);
  resultdiv.empty();
  if (result.length == 0) {
    resultdiv.append('<p class="">No results found.</p>');
  } else if (result.length == 1) {
    resultdiv.append('<p class="">Found '+result.length+' result</p>');
  } else {
    resultdiv.append('<p class="">Found '+result.length+' results</p>');
  }
  //Loop through, match, and add results
  for (var item in result) {
    var ref = result[item].ref;
    var searchitem = '<div class="result"><p><a href="/UMSumSem'+store[ref].link+'?q='+query+'">'+store[ref].title+'</a></p></div>';
    resultdiv.append(searchitem);
  }
}

$(document).ready(function() {
  if (qd.q) {
    $('input#search').val(qd.q[0]);
    doSearch();
  }
  $('input#search').on('keyup', doSearch);
});
