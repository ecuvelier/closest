# -*- coding: utf-8 -*-
"""
Created on Mon Jul 11 10:46:48 2016

@author: edcuvelier
"""

#import mathTools.field as field

import secretsharing
import gmpy

p512 = gmpy.mpz(9319634055120059806745748435708214381572549431685774586671626637293434870481509294390553200298221079261837854412673960748108983618275089950667346940668503L)
# 512 bit long prime
p1024 = gmpy.mpz(167780332417814791557185633280139094620399701270919685281072661484806859644138201313993771306912137951599884892086618860348074919967218594952879647759290846287306614649975347611649907631145784217353653507866496320995387982967013950048825794409156202596180959359044007356986797940576989969403213060035412266103L)
# 1024 bit long prime
p2048 = gmpy.mpz(25470863719506445965075708354842107079884472650917771904021312045515220817417829515566709610109324303465461055432109006852236264861183112224977782911020928879118877401841120368392592182122340161519445975767856835669124012730950619704221016829258214575328653215513658082947894192466547032909169462559951013658605607416084963816031733602131783737713557467711049947600732765469680694980354036750452839633158342343281937462940531128893095166317622982135219104382743092946903628482092994756550387431788462546691099242369662804189941944982531651939152066912922798062738180568924256478351280742360606242522586581950669965699L)
# 2048 bit long prime
p4096 = gmpy.mpz(921629896787945998651227620043239546596666276406476071639023278383824510783893240935595541307812013091050923887521049077768439156719992897132781251696799414137580956731811073261306783312697795057081221809000762189285114076184466695226819581712448075024616534148639975327629860998751398311146525753981790056893898957118582467750050428004910822024528223803017782057603128662226507252269779258719676911892172164080054973965316693792510606717600718654184838581621613080284387885546948258873893548793995188364616309128273691690028885740711192851638758530010265230258792972108882071566621980576208543346861132693204808855621758282363778762051552414179680974679123101400358237601342506860131539413302176842865847611929274931677048948816387213125465100346751981092172459844769325178199307508927671679405104246394264091735562643130119948126023382293660050290458688530348035960558250841069580560422879427005581833101577863920448541772801900684124066777824739955929726393133533280524668690328555349462327895650451867040891210125835513327765100194472364016509884880421036098703442706344617748909903411847601902126128170835180454431397772997408604937677590169909547986868659771802399498539689577625833915273175445729580176332714163380874741339047L)
# 4096 bit long prime
p8192 = gmpy.mpz(1529482812413151636114343411795915979139807496027108776135525941187247029153130537807712633943767583592857748578256053608465015252984523978977763179196699284475063742076513419805724968073415891975961441453800846422209256645059840369415340994988573047147611705537390995833353867637098044497270796178233350894600518874674385403454357175825486578781520088360819705899433930308139122346882217332062989933564158095050172502276024912170484923490836507196337601749481529710002067891673033299073226544227446669588159870922246839106068065852422544383407575852026850604985283465068025649319357314778826526149862681322315146129826922463079455561972038000455667981563022197497895513189489637628544902868018210199530885611602007289661987259864309431559546747903693845560716254193928640238463516507863110764324139123407379488107534769725394915591443135108402366773731668898315786847565764601304784402511097418439756313339143631612502619203699644712241762576345081603464722808314593528869092265303413622484506746559179446541748432725595930907784313584182497207225977090815390251021534275716968169875172323349050888732692491174024282869883165384109575779842418115299920036931140248122794897739666828449749760601071328663183455422095768692643981173932312469890012842795598959614468149494887516185618429721629673898343437352699521518364432108347371828682628782894985582277544436439641330715957820649449602128227087508135889058939167049559370984537288968832056078998050050956780334219144563290012911577132017070662082088065291025792160983265998837428798997350035777083068597670969958933450154480812041803167271813911155488568232748461163139888921218421640934573852764105086686865252286683423258271576888832331986969716174222199217462740361033218377817143640720185249251216984428303857850374665063195262750715025345532007259275857250959073255412964832295612169254821589969355174164559891720962653589596985210609959450852787665439145249212338915427496855968529732394059431081719507262915439735485238466018180796192559973419840444698178349671779012858566149213147595172757478231105515186404807712383706998528700850650734492108114833968130706019434757178682097550211260013479364811440654002286723753989801027035914028868393347329607460230759199560494036602264816913286857076767750685774407097524934276547917456387473218711591167587472037282408108356967704901217871712252213841633092619486761511515334752115635760923346123882369827623526418386253708404844575432325051213733062850131021663941L)
# 8192-bit long prime
p16384 = gmpy.mpz(1140305476314610696645029532268875953382014019458260883147358149750612367307202600650912519511881356343827036285562292836067819838175415747757790654120786999862496774276525967978176646798569048629631386397226260317474145539826806576197186586070229671972822768362615432323760786230733219689226180721360776397912480392629097553611409775691891640337016075202091380405749523434816816850434624104473757537325085328923663814100588974067298741519361223242500655206119243051966532970361839055070486278747915320891378498448527028467349872449811430648851045525231602573565851062853342331216960251294395093377346143982011991518900604707303260479726991331201501797980040474920553830648053225870163766308124898438546707527070829168483743232781891544884527610958585154817815031725253973979595607199246852549628604637555032944887460316945250010847798059180770168891201927138718262975949008019730525000438868333217142453894545211774687310149895255184025601722558905541450483931546111618364202180233013325602400471923597834448890031390787380698124259558844566103170548511732219102669539063819876032033723179420233270394046166586070432622124999876097745992150277318270421458292991260941485640711612845931136730828279247665093621482146873301026409581801557236351746943664208058462160821565100017000182958660126734449918552839797874763922452772057939740679083908342285123225301791933765851160140599974765673856776755556496639761761064215489344893702715842407127896412579286744398625389784551327166475380975586360446136983487567902988992897100075042454263253838673784813649812777982951225691978865698265739198273344165005466341421303561923173769188332278210409934472971407353212270479940595616091050440566010811387693333420254134174916669992051859599631685596389086752701801294558795414508885641281426114254344411540204214773157366635960820714170839527285263466443974222383088271005149060528349396135599164107944199112028559360761728305757648614331723222633866398067813748306568864037032634891138039891855191099767192892387082046946406671239410629356227052172698681554014963328199790590197938715568425701096444130929500538673642301679631929860550450830951285753639846914085867984277760909915379087842211576061897595151246859373767570707631769306132596214775245343952651637640601900715970742021692188007280606930789445084518879751218983143441900158462363727585766418316654810778605482522245468391479925053876712012228393778410083425337148288319121530969541062332712773436250887131971715423220985292634642141139812158156355117205726125758095344102647502387988361692096615000562838154250645726372364303276221060246164261101720801754467284427544464529846557471958107114812565769565731902318473072038018130440201669202607191385307070597031169828188862972498508876495056563736078864807107903291367541638460109759107486994870124824185788266271391107469614130753516353904298075940694870726208369236358267732075147114416717707999659365848565659030791508828453480530512424316975330212645805549260518900604850678937976626964233758132647908294406964771494488782383827147196016328456817185610836845914703166111120309024626428065288693613944086706913331314564351603371949058720423813201531094042337047523818736894089999692254131030323069315312808668187806100913227580642598268187678706988505811636154106773795034456759723559894123080555747950240457772359452956153819548630356297187889468306936525900044097781850788407738096256969723123111591817883337389290938280337707502734194434485644227822343226675957399348475087361291772992607990390078311347068001136752835298642887960363543867446810295711149415359141971074382076256097510626944147272156612139456300601658895643947275872839765591700482011388610351490701617964178872444126156938642991182705084084803490724579109298861946557954728181621559577974788555023211975951274462896477667244279063105770902405232773527099861103790916975642932852549672609853282367324640094489518130207112278371442453704937000976398339427465704822874229817990899581050622059903326672360975219438651886536258860092955785638849655758882720938201258422318971010068286518241794217157940857051238804304770637069765460791514023097776194822860853820416334030297188504944103140721711921700609378858304379967958497178362132505394075698828829957974964515718920014362279399555546256392715421840571572750726598723956927985878432802613874943929149999378361291758291055313886083726300611099989387888138460310932918125321841451093855066910532910523498395149576702610181460961648806365651354776240915843433624847653092070025479742433671011501879354968308722744215895954711353042248154056586643020451091196652355767750165819937930272432879149528621204140900846565634186458392590698394232377635534515931575023606012182283623905350479652590198527455192180283505802135131205328228277878744981896362854195090838062705986641296248507117738877387969263516867050457531481448809344918025222313446614873389061061619612523660849867561194032834640307898548019627458716761L)
# 16384-bit long prime
p32768 = gmpy.mpz(707730515522477394500776513872475800674065355736194083617192874136183317120422626798012678238324207537737936480828063246194904289772368924440969148125436595871963896772456505525081325638978514923480105891621466760603772706742484928425925570644257581600741497694527548730311049317837501676964612139291467832208131286386654076638757173240156685994306314740741781219089464479433888925036099158087420625977795498336009322546820425401839815110183600691922433395724642368759131406561541719518621839220210448569961889139476385156159389164502447273532744538798417698008576801585025185651007381221936350555689777242154859331153441888005237674220746800245971739520635996460097665991532465053082363620719470438842582329474327443085820562236987813120816375075063327684990510646785033021152741243020441582817931417864318523029176201878042872845619736948945999542988172601852329983578713619767918253566828454407623040069597784730536003150795186477415369322195569008032672065565603802132026948720414452331023591617188773713643845970870767973255441495452238931592736899264194030228784463971816961964436340963751014786481565420427426869968538440517823089691527741716938025701018807212374451484509079593259905525772683983551883591409854567739509565841654665398687204098669915763619520357954056106547563385358803000644449444685355448124431180751934602607268454129098460882796532662696418166071297205567301737754683014072845153175300929647630648131665509341138158783874767285529386117783839778460120394554535260626993565515631951146517372183678466254976094414237681155658222642114320244710904631869211815465621512457293931964067359593052082330302678000795981389323189147706829885391323489618144531308221209035785519641275644674424137261446529780858930097017349120902443765637539054801818580247953789997683209818208514463786695835290398409263037113047507187594719289608035838770383042802802053061518334833717338861736337782229495835634207050400515726958868332973642478337442017653310643232591899346926299901662309932590928122211039616843647254268204260543709436954249101355298540237240124909429005745465259256356899401814550819358139289437072607214513093138301144506242263415038323678414382439163863359908214339452103972228447196592991545173522588443366163126956148824762219940201850715283380690179962779261359100977143758793683623755388839467332236274323893524153165385431185007762929002739878235749613622450571402874884782092376605983611613106482082839428302446208492457548711480267061166726938490639621782883195898155802574611314164127666530771938762923014702253564445026594721263772332570756785568093563437457300834875196243050253784221023415890315516270287038972137227114043819620868409252581879955182565995316473731496602292609061215996161932122473697195219328178212018735966242226093272846051251739535299976911582597105509848380287632213401424151515902152866766114025090143017087584459413730313021134329147570353457523594524746289498325247002941168535575002434478096703296592419316847034204911951718572208688019587117505526614423425712108977586451459325501805492054201325464679698152817156523544362556519538405970045054927789142968914582106788306411105173978872973665523741262673301271326588449904639404116398278765916075124884626800333951134014830850074816434270978133059764021243267007389389923490880516577503631365081337977260110943692355193525860914635958796147528584794769853180835541047404702935895234311617447957398232195009629583756885932416434518007822771097504228049307519174014200401502900972478578141373189769735125301877732679393140738043022283946857565317957473042680806186371366319018686143816948559151625018177948879104784505123025781714554627932469122762275100290109137157404869037511387825610187052613607953102646375959333530237664296612683896530535211054366900491927753795903206730482292797658179985589642141802365734334272742380690873795819868226709948224661743198515388198880601295233818752736695111124728362046619341278881390919765469116875640999804355678073917827597618333028177839420944931142007337029526497585110355702222506383321101657296185856297438984171632605116399067511649558659095885182561903543352190904879801130075806498448497147093042237809569060727647194792937118895817350648062275089836029742919128222923265299568831240420672188251994622316672508035443599060210717787863118594656080909010774003194750591196720856071022476536132008338399505812310156123234277327185772358677613870078814543369855337922604996066671017572019480532946326696091437811466335033899216967445854759938925397109745723994080085966165503247810140047074732189725076542703112540735939792947043958046070811876172556375533851583201840581165960145870423694478816155526671213076473662005813961112939269967511487308031387419555244540047087486420534051003322838749646884545681426859650479387611044335454861947707433232200378157235140981017138265756272004863087324699968790869859058991208680492979129734242718293366843329885515338832338952700761180020946240975727067680270458705549206143361915336356455301693374068174439028272873056071055558329992891199137813561224707153570374702442030376931853012140515742769333066666417798908757308165864059491090314411828834334049810899921005579010383886396456149384392807287208009660273098396743009338942275357935304002494414989074483490385068442176613474926827270827918514749008515542971830220233038009739717590522718448922675524394220051134338899128567387040837178597679423880613301826520136992720991110659043907917553658785605920607912803226674260548968206760147999130375520389351870183154935999557358720534591412891498149705811543707504455470651642091065792399908105364017127777843978392643943549470963868799579912199263786711558864126419884459572509058997798973141132473261870845590429220597186693549484765063417007461828313924564531094572786435106112954732265459765817045103185573160831898639902880014247644042424089690026965717802091258758300411968368959957987051795583819449435877009235086294617494698525946514287182644445151890119597311269107766106367777649698771422675314680780173597729643364780584117691714465414189443839098795312055186133669378334207449763069240433373557415707343789845818010293006817837779516744324860531122071393980202028480653088011490621420492412710898575196954856942495354004327163779012809537106635357126215757585819497252860072173751092924264064500027814851711347712523604759088788564255657746029806861183362307671984178666462095589020978376566470798161050625208534406988651749016970306895549860087393386922348367017005134569776939106193554254079311419866796817459487808306684121941404195754622403404668941482669350772752345794758825236119790377094773824895019013253353854881549074373262015506900265945438429113680250838080937330973215823964786277996483649276735576346735726240059948804086668376630062226255407666708204678514816632586307101831663204988076551233541689564794056418640355555673245449473904201031200614481597081355828711499214631789638257707000489526870331366908316490754267564259220129003391196144430451911603718410396520940953546895937458817914927404075320447453563800215092601150728699246766555959497050426876885978146715081283005680581584476731094005115909500106834890223928435624282188792254542944398941873769154590905350307516112781545508344737390126706285669312790908960530774676278794161829781337825281767593072377216778269873549161321804771243060256458731853356529532115381462176808986026746263559596329085925672978850386285920999088018134699944506240372537962490239695174666367051387200004060036730770270285525753485501952311742172381002563172952732946908947688964069798274968360050245006687978302944600383798344032980538001736002792945111297327505215061563675832658431331742392983223131870312282437675820390461851503434053720395135841468021652436789824494989285877449420394592240064785223495514752379308196553243761660656253727018404333605036801072145025309805307369069771642824673493196606551228431896832756266827965970895268809510302365300721590625331009843745855773680298558928488620408555019868576677606227372953893565589789328235283767525096351173869826656145261252935806448995214980928775015516832862823993991375934203647365218659752667891212645162213997154187480403342217708222953908553584149171472591492797055640749736247874750821209021367340579280225120654639531908373033508137397730916387349503887211947874338807697924246882836135978639332273171580804563405014127107329816812611967254465845864292014171178334666317729039978573916894750848417890874117442459546787138165177288920987624801949552703552447893799131815339603313898216877022798704588251219433800268508439584957237377420012155961084823694189976401261923540051219642556282875838863186600844201627233394535356787607128096226224514555020268997313712266201810089940028259360609554385687036819059359536605683647757188354298268647102272049951795377185828089328480085108837916076634082295837002250119536871751324049552812274293746772412739635294871247247590611861164846672734319653495261559497820283521265684788565556579513690904035673495802256953225199109713150449602331217746289242833276987246361586929888742706463508034170757758718557568525186375139639274166399596899700077083221400713655038268510059968036747610987395969879923084471027698678674139089025220512245002946909128479332694485600661465840286923042262508166112323433308745416248042495845085791514676304918245454056732334171914992675795276472642186286989147742548975446536211759302991042743577235077512634512927022323248286224247612671548130948189465741441643328754429614434243922092239543769226987072093502442183280628361702386095423793004271980674535565595854471647668832192092266387330751622955128725961757803855779852739066278020098831707455942571848992732403654648501455125252651143884706168720599680212259580358276445441408398189148440820913990726517603616876031759391389246871913854054956746581466091213813630523140084134979038770561334052316856223697L)
# 32768-bit long prime
p65536 = gmpy.mpz(1001764965203423232489536175780127875223912737784875709632508486855447029778155726544753065440466674050519117171453631590911474691059406334434753182380773514582520935958175793983173609721465463991042154552427995285079659479819762431686183601501458484796078054382474444627045402955728518837604250103335781851183063179873572403555887407940457067871360483595075918141280309045729426349913070712515061695554136801921883938224521602980189562245452853780157017538081281238015931896563242351871891477487806885490802307206654346059051242979576190097665515146081400080284335052825823375284019370764731921122422646268680721266807186864544151897300637362479207432457965323626007577846961314090345825398190532066137653633571999079254405646314450567118891352783710540035032641981661077538915607144275837777036672553606556213699781491359884575027441952611902178522924098978196578926755009496000012070981853406779920232019736097008034758845078059863491168945008820758595025566733153449070109691740717713193653269776484845694012079080929780550320181059898050929767401393583600061302321246192555696700232175811933783539372629732335451943273871741608948506382227764704546010979792875811486666788079776197442648789977014235971764956771881852993464456878576870000993197166232445026271553314834582621709587345694816238280144707599887738851569032390671154798095480327295650445094443794042366812978032722444250723667853029408545081054249857264784172030989845282734906815581026789684895701618164248116523210533068100110087893925928704581025244855890910200093641469971723093112164004918661882465907394924059726356503720110382840455188101999601746011953313132245954583992730757889419530198860379639689426120647150508729043431131684642362925701519807779282165192725344326106557406819204192389131895229803593438364254881735635994445340239121615197359325262830489075364930570715152908463962485704580529708592676137943752238796109150579390350987767861120700009774051002830886794890749766162604294876731773503893345203214508381904080870275202558835046836601402274669513996245933653269965820360246119237407640309583450466902866060408175353817175834934812510484511581429675035937095289580620768448757404130952423973285868300502946238327722920419167395272072408842127663603657793174673802568709889762595182516099010054382369184341265512591688766954430713092400187004041119052038234439235823776472663473830850212230531655619010567294347266100058282038163511537146213025791405535193509172662283817812975715016018716370390439528141831703482515422112927983519635934730579256896693237849874284335039911980302196739425430824630152472530871706182914176072403363338420903541877431105704118289901480600013720662219216201165628701772509676214388215440116425427943044981387229082340428937557903507371881933988477524995821999142178645207689071719423651742130951694420747015683069927128817788552667790103311092788530041275644446666113218140992419306619785338095704819266916187171879415429616861142322143998122802738466214499216326338689186586644031605376605619340302337354214025583244354542385145604080552456277799161183122434278325701342320604847491295282759608094052170613419498141535827434262768457425149769837751977469185926702950048093744736996440216248186582876901836793355087891997409235899249123474030266040998033091717006238048319759889010720599876273352040304249672089128142546363261854949325769731096502303682253963106487958849146946183507585496045765783907219895624237853118902300004959146660653440285023295729193604044008443722917778963129232562381543574283156764467083058745308763335746336088064165422636968234622291446285694438919528150241241899919846014611107743072951186739111341260819978720400863572073089779613087541944510037084963119150141143124642091335621702875712094284997136165803499356493441385910308607226571287472007533069731584598814590753289872763118095612424031945016834537182994613174782057332751531482980099860318101301760958888370334388731774687659449793933141062734898551032873616360686459072333329710936001737254471415455767594635557143554188079611190138302663911675830777574684687889233335072858985950613558906390225120013192379394169698408981475345399408560845343464769124264915011738034227057089069555324280118274877113748615503807565935012026955255456908921860895711264293716049262478939017341851668909210722008569344062124992209309064635599266657691283660935210765315598874267607335477667313168305432333666146204939924628345554758071809300774454870120956754811521806098064082975259333011015357806842366182330434452507131956953257531954099689426159182529948649562702239721712583387149829905924616575777636441637014176344221204376405641644990312956336849773123670771666750073615715306375195153698567626034669086921661475350524530933769716565392399007827565192379077842618109005209825127798090967493157956616518048230952995118056340598011720921681667297463815973050858326456911858591197149608136269230888032847271148938535691599408518482294344905931605488450177867942312232417853145726526378550639436013982682239862012702724066374195897064413211917585974598604898572968443768599364565415869016955508064273707688688857975864042055813798593192462111401186720962734995991836096065643517792653983471356708195516941377159306821745050471598704523665507238149930862712211677806118717857912966691402493121946249111390357975881378923554737559516741120706012591344356864096552126739098064220088239765752528555361487157284957611725821560924328787893264098782421754479192361461767279732260607915828875735649354112954646327819418325560340971918452058126334355022280121852100331854500970592778580236022321848466425030023464070253559534630696996951367767272783735157451943011012319974130250881215984652820333183313045103524443719449453749076432722190931458691450525910434968191330934151957636632290643391403300668750048296682312573045861590156465173938710617339559227395655554948897324108461252814699978396741900849578719850268771067242937293428023643375532711670946919549555293232797556823030527578419270608729900903566581806286539805584171931883833653677291747394894158165064620400418178412969578556565489015258220858341259173286837967099042479473970491646250043194889281747346606236713051531356872538643078461298314286928952766620320924509225664142316354634876915433654204571123829737219986674065405493199708689894828505343513367080983598295799794268917411494135062802921182794769845153237482792073990655498578771021628197888035242550440789145704125388869279895064564703654731392972252929706136597406376612576162400751733259524114480703323445152551255458118885224243115114744483355690277803978310366224686687013918383650101505807613504460921757826060689607874103429678460395107251138566549993864729798476408522291090978040482905851399031334945602530780371162843421135653147504932210926735405203564458823453275418064958347389011911251394833921744599704828680852293393121277003471258346989646312357262472704429211363076877630035952168164598187888751088002597900346923817894793439244768436061449278903413259096351816049740077937227787587656368235710647768247042192793307604006057539537534276672244629346641929826506636023485347285773479676829285894447431166646232601367926594266685474227701668282678494086291264459028317744181871896674205922790084165913838417323145997802756735019573938404320161314808320780333754076855323361554230982123768745276872402659113001355108200490292248763011517820019041736026574970586482868392533210700421348248551620959591060606603469884571961684187354614133869354066118340043462351745793420495576549157706031783061593752152733768491615413983228708810403296588632842920840918983053072481716272055853470850111328908679175629910540384550980526114631939872524509627155950310280953288726208095956593766992024671988411655149232946659186507904796261414603410431115166292640059633248157220658221386501618896137356165348208574972766130517737572815645334427172713434894223871490888746855058807325812091808340127407648167654245424971503381827403051470047346875304922794279021985242957224792222539989248522791775342704372581658232059041561539852194924595253293793212905369211210295595970837091245226350144131991528975028670855743515593571417092249576728351457640052242572588027653485720880684291192051393829662331344989209159810156131210588695738604002441789166784602266967976627282448514279294867752875617564768270251421040511392624388301787123183336574340139743026222891336813115426489132528557312423297957105139061394470724081997486940942311384122425811025908538361084931632850827158459871325615020878664952236768836268422896377182706413276790929023420034683859302510035273623774200402765212475927247633623630673659087371090039287346732723568018487942059014704019808373473144270339586069300612709751909852269208634003199410328164396419791354255459979419724148887823576013066435544763081708853575821449743976782427276776574377489067004982427249317912423845295016558480651883063961732161564853314205653713523101016006684175192712680156818381787606302353712655604616701418741474726552363709484643637786013807636134141688370696712826326641534234998798548875002780444966342512524606442034137069940815770228245175387935840037027842862010879342719526614066885353707915378134814158477843712030263863242926525305678192425982959484324798167784108487718810715389332967365225082411216482445635354949038338312835758634531029407774833191286914637091041139480342244111491697408335492019512141757153406883626730063003634631484734336375397173095219998309489805964375259721178201322151635868670795640748028084176994094284742022671155712306779962636165032440813733361761875617155946721059442542539679081924497243772378165844606934837787151368976892631271164512440523590969518610333447351102129418447920469999226780474434973416926289837580941079705490812459370906682363482561990338780973956278978723235713934312026875288052102133574683042490119137340287991295665503459970952325953265585954463038974559608973203677564816932261517836672794016656598540182728592395775216327449779852931444143433303309010941124301072499986561082069085326740087755219203312206411401808324452128688820478163241412629203834522804219745162645263168766158254543840668307121199154765403274830939690974560016959744747032566199408321040044197777471118548367420036321352850582544537598077685093132398728190593928087728556700236905381381507476654867587090327739556330469017155689266266441766676012467182989564670642427485473413164537915096536332668891279657165555481924026970429641994453898105239923959843438269993738547956394363737937219903389912484139136100463224972279690207304385320970905220379134902844019474827308293991952330293822670905144953597146510887259988052247521598420751727757022410464466689328681526415309995038874363461499304139526585845938289430454470908528996702445109220779895546338431398298791976241963367441817372825843508083120321212120614480559005307841171269696090026241727361889609955614297957095938745896911670005039064163253355140890698014560457360050473939376275631686442111176934745033963832255817379050596937659828621060738019142387387285852289305208692873955650954291938945076167171506502641398519290179907591464800152841306045975471868662727085528191943523764475281980514921820680467820816294704068990755846669309898669910835380502303990048008012411548471521903478310061606825070274793125307641294016511454192906239234657860161616800949734718823863360939688413215914191301782260349734315108024437264212181796779311166753117972501445279290805637670891875227968063065426320414025606936588745100124776369367292978202580415291526885366266985776310222352714786769180556838761584986370146470837102211624056937537815659539136094432026687347106921084964431470239817652575280394063183103248615628789509799436520597813113671864450258280555547055872638982741395235625290999538749031910779688442773249411469492704145662564538239193161247390508376745846744644052101507805141693071913689080473170667691789170382657160708575327938773910126227390328650671138735308372120984476306582137052347737310741878144149885902093392542273482809575454347937125592217918653295475730490225623704705686949963911246491683898005507693548064874852783150818653601375367379961471896196912213710593079118080658943196276547558594210649254153619129864572071125789701941505679541665825929117483610629810906253529056879747762511373637337184943565963335384649599542233580614369429228792311363286665376867786411975808482087599337506340872714661869147071912407188569930953358328786472903902410279755940843594037606485916318221077668393875637383470395058528754909787542281782608694772089937537261927227600066786016666189947537196952656459106127629916895454731815101092676924427412531448857808481930356191385862810656730274700885206790865965881685068166126409563773595721725460355924419183409087131671474805935045751524582669732381858883219560399173747313698911085751045335095151234881075639260978071035403230815686618258926988146046012750144481006485070689820019027867474634536767572980604337398273866846479386814317830071883982019215398432069281723900664130642294592449264024024422090410819711987007181451740832729057227183230016245309381519751178201022265374105120683447598322110669600378739564341902587575317331284695968870141756037833130414945245938643916926089261396022885923482927639395223781096331996004204651037836962681867814195414908788951076601053204808686641799247033326070599091905442257729886447582286065948898953745970506574184272319808452303515053798409466870608787994082563500380631394584755203157928818767393710035111025535445628806180829013403407929249926315732939043308400366632338415103195848601532447202814097703095342621001526731578310945663654534843676590820547257144018302997610124124443355777214552360964567124173219352684254324374549589406335282832693595524860910021185746370082230471729922696268353066105308266542831010594484117002876337743050738496844369104792276105785961739843444080426815807931440075197974709264744613537205414103584651693909042468102009127611135505492826722408603735378009622957799715536474789098939295289470026270061433758571255592178218592026781512090612736633046651355198984045532469636361341517705233816295677639841918852509927617310611429205278559960865858984902169658853875377813528023915889922223818780127318516684623557110407759986845685987581620651374356099931702274124262285059276671337632357989155365622831714902610727747078126362014457666677174670608931018503630157639935385936245617247238573954760367380692712742655776386650515171238417932748046861162003577259064866346040529212045278862822901840731117246594854069448571649915673808899839856226891155351869575736939346059593783350159660640948401661348297229643105303719413708459732581133816270332535440535515197089430282446884908367079512962597305911821472826334686101577752350106799423146379006263857711008314977431565162456155514813961861949883208401748570613263965953818163068407072758188328279919894244690866541334389950981443466148298689975965810593607727643697085121834942796944396658372266681559770759202044141907596710617061410015475156670525352380079993992736264595332611239659857720165897418418686610410942886670811928220690350270956765122971956751277265943227398126130125881464187165232551180528791757275369721669805108114837730707890563598500869305747139750705626640310627387905256486044232631579047403316843835073655366770358855438307967928407049106483865379598691486720722628344385427662285444479160496911716051359112057381866395678784307710626424828951667546576388462752922822005276096322252656036878143872499081823166417908070165087906983679713663845224460180940193377477875903445029266463600746961750262922573353491314274128941633699367610228614119645103572411109942793551448495967936537138907579878810382011975621930101016298298125106289174978855042813193059116906659254507343288532005338139308791886386447946373019701965168635936925268456478563357533448344246940442571471804981006483379539612541137656906424925763451465850131568164471047898788979663817765581033376744325658661936219374031756657256322444983794914406462740038212593293245120555563650678598590690801291589253466122003999328317685772044227433196590854197867890399529865419547440902030467979595453736980452205075258160874840706050382859588741883677875500366808461193268714539728901600021168726403783076521464507247890314817069191775891799882354425674502428486848982619347922997297796045354529478445725570706342252731058972513305875083464130125475385389105975216308691611781218800888399681398049684487595697482516679253577709218228426308337121844460185518747664212963565805268917490370369579316908983829212629018368603234675624326119240670831904030752852414529945348225968220009298560212861503658205004958493762130188681088881715310808372442465405464950504758987270782125602411043357293424627566222133388563931864105665768112150545912195621690107023121111674576779758445408144243994994136815222686216087140107877888983510833158523984864086241696420507821137253635889634699964870154036385197506790772571247024513268052912704686557326552471691242189859303468607222300413399001235614744702880926946101712804151348526438310688686797197112057353537036451362730653679270872845709723243812178841198532851592084233770366733173146836991810002020700357027138816240066371101342696849434893803504795024342325313385681535489910503278642550653300505390316871672386536739326940871340615371883033321656387678233289301857596461384220229136641621904106420609388066021230232450400527365713374630413461077818702743120858515513959998471322810477809908227273831022511205724702374674916103403595676383993373906729101929785206733088968614267470015815799772046842044786266719351493358914885186666403400882319751045011970965749557504552638410559755499531583075155792791417791303589705026264291805684980651721395086905893706030644091031011631924930757828225615023896483781809172884052521670884771533769020556964276896264620673669740525266012854364093153645579455667971007380936332145782018185963801153141920325212720871167732274993527659363443963212051073681849312731873579872177471721949865025871262555438678943195473406048336714076292959962428820244027535664907149679955731619959556979963376288179503723286405095902920903671113867360698861609115885858458200054413056274546680593390287861195509093084274554250442636137187106043262426186228124348831122692409649335564726472757748515292959653599248552707090818484488065563372013504824333772967283529968497732250279460814023988182843066658281953697851636017194587707633750457505599428436354424097765838465840636446071515688409008222738683759176748928962138231677081216800562980126054750806132055173041732824117798967137028434424612229372746888376060162351901517745578772415647637945969946840438163842719384778847440711422155999297850363760696588418915885169565211530479499568657342284505211047580983535253210128366936723057827638087996363575938830005119472380269894758472854401364368112560538112045905033350441737368802578142766971782921878135620622228825831532042969753973775460231966122601267731817222395877830862981093599639593287745428926475006420114517530757468655053504723075505806856211880713361270866027979601391064662862973573208612488660658190922663277639802135270935748118292626229324466627072531321168942825732335302149282390984230796831644477149890361271132395200308009875987503730272575030145903319135748508055493975668316885689217208097026560722645927590068287779333807509686514845966038060004627532540791637754249670384398626184993511783965513402068372859478320715926339527358584981495181507772822545022401394527850984164156815359498849576583339604479384286145300457736459818190836798336979987855163007785960118674290260564058729305032576299441921557255947440276064572887849573288765020692358562288982524087928197536447668769877911043888753036169722793947952859615723L)
# 65536-bit long prime

SSS = secretsharing.ShamirSecretSharing(p512,3,5)
a = SSS.F.random()
print 'a',a

SL = SSS.share(a)



    
f = open('test.png.tar.gz','r')
s = f.read()
f.close()
