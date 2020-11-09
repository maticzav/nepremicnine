import puppeteer from 'puppeteer'

const CREDS = {
  username: 'maticzav',
  password: 'ac8b2a34',
}

/**
 * Reserve all the spots available.
 */

;(async () => {
  const browser = await puppeteer.launch({
    // executablePath: 'google-chrome-stable',
    headless: false,
    // args: [
    //   // Required for Docker version of Puppeteer
    //   '--no-sandbox',
    //   '--disable-setuid-sandbox',
    //   // This will write shared memory files into /tmp instead of /dev/shm,
    //   // because Docker’s default for /dev/shm is 64MB
    //   '--disable-dev-shm-usage',
    // ],
  })

  const page = await browser.newPage()
  await page.goto('https://bizi.si')

  console.log('Logging in!')

  /* Login */
  await page.waitForSelector('#ctl00_LoginStatus1_PanelAnon > a')

  await page.evaluate((_) => {
    // @ts-ignore
    showLoginModal()
  })

  console.log('Typing...')

  await page.waitForSelector('.login-form')
  await page.waitForTimeout(1000)

  await page.type(
    '#ctl00_loginBoxPopup_loginBoxAlt_tbUserName',
    CREDS.username,
    {
      delay: 1,
    },
  )
  await page.type(
    '#ctl00_loginBoxPopup_loginBoxAlt_tbPassword',
    CREDS.password,
    {
      delay: 1,
    },
  )

  await page.click('#ctl00_loginBoxPopup_loginBoxAlt_btnLogin')

  console.log('Waiting...')

  console.log('Logged in!')

  /* Find data */

  await page.goto('https://www.bizi.si/napredno-iskanje/')

  console.log('Searching...')

  await page.waitForSelector('#ctl00_SearchAdvanced1_btnPoisciPodjetja')

  await page.select('#ctl00_SearchAdvanced1_SteviloZaposlenihOd', '07')
  await page.waitForTimeout(1000)
  await page.click('#ctl00_SearchAdvanced1_btnPoisciPodjetja')

  console.log('Displaying results...')

  // await page.waitForNavigation()

  // javascript: setTimeout(
  //   "__doPostBack('ctl00$SearchAdvanced1$SteviloZaposlenihOd','')",
  //   0,
  // )
  /* Reserve */
  // await page.waitFor('input#selectAllSwitch1')
  // await page.click('input#selectAllSwitch1')
  // await page.click('.card.rounded-0 button')

  // await page.waitFor('#feedback.toast')

  // await page.click('a[href="/rezervacije-odjava"]')

  // await browser.close()
})()
