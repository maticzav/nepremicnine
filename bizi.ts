import puppeteer from 'puppeteer'

const URL = 'https://bizi.si'
const CREDS = {
    username: "maticzav",
    password: "ac8b2a34"
}

/**
 * Reserve all the spots available.
 */

;(async () => {
  const browser = await puppeteer.launch({
    executablePath: 'google-chrome-stable',
    headless: false,
    args: [
      // Required for Docker version of Puppeteer
      '--no-sandbox',
      '--disable-setuid-sandbox',
      // This will write shared memory files into /tmp instead of /dev/shm,
      // because Docker’s default for /dev/shm is 64MB
      '--disable-dev-shm-usage',
    ],
  })


    const page = await browser.newPage()
    await page.goto(URL)

    console.log('Logging in!')

    /* Login */
    await page.waitForSelector('#ctl00_LoginStatus1_PanelAnon')

    console.log("Typing...")

    await page.click("#ctl00_LoginStatus1_PanelAnon > a")

    await page.type('#ctl00_loginBoxPopup_loginBoxAlt_tbUserName', CREDS.username)
    await page.type('#ctl00_loginBoxPopup_loginBoxAlt_tbPassword', CREDS.password)

    await page.click("#ctl00_loginBoxPopup_loginBoxAlt_btnLogin")

    console.log("Waiting...")

    /* Wait for authenticated page */
    await page.waitForSelector("#ctl00_Search1_tbSearchWhat")

    console.log("Logged in!")

    /* Reserve */
    // await page.waitFor('input#selectAllSwitch1')
    // await page.click('input#selectAllSwitch1')
    // await page.click('.card.rounded-0 button')

    // await page.waitFor('#feedback.toast')

    // await page.click('a[href="/rezervacije-odjava"]')




//   await browser.close()
})()