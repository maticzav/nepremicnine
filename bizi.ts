import puppeteer from 'puppeteer'
import * as fs from 'fs'
import * as path from 'path'

/* Nastavitve */

const CREDS = {
  username: 'username',
  password: 'password',
}

/* Struktura podatkov */

let tabele: string[] = []

let podjetja: Podjetje[] = []

type Podjetje = {
  id: string // maticna stevilka
  ime: string // naziv
  obina: string
  stevilo_zaposlenih: string
  dobicek: string
}

/* Zbiralec podatkov */
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

  await page.type('#ctl00_loginBoxPopup_loginBoxAlt_tbUserName', CREDS.username)
  await page.type('#ctl00_loginBoxPopup_loginBoxAlt_tbPassword', CREDS.password)

  await page.click('#ctl00_loginBoxPopup_loginBoxAlt_btnLogin')

  console.log('Waiting...')

  console.log('Logged in!')

  /* Fill in the search parameters. */

  await page.goto('https://www.bizi.si/napredno-iskanje/')

  console.log('Searching...')

  await page.waitForSelector('#ctl00_SearchAdvanced1_btnPoisciPodjetja')

  await page.select('#ctl00_SearchAdvanced1_SteviloZaposlenihOd', '07')
  await page.waitForTimeout(1000)

  await page.evaluate(() => {
    // @ts-ignore
    __doPostBack('ctl00$SearchAdvanced1$btnPoisciPodjetja', '')
  })

  console.log('Displaying results...')

  /* Find all the data */
  while (true) {
    await page.waitForSelector('#divResults')
    await page.waitForTimeout(1000)

    /* Extract results */
    /* prettier-ignore */
    const table = await page.evaluate(() => document.querySelector('#divResults').outerHTML)
    tabele.push(table)

    /* Save tables to file. */
    const file = path.join(__dirname, 'podatki/bizi/tabele.json')
    fs.writeFileSync(file, JSON.stringify(tabele, null, 4))

    console.log('Saved tables....')

    // const $table = await page.$('#divResults')

    // /* Extract information company information. */
    // $table.$$()

    // if (!$table) throw new Error('Something went wrong...')

    /* Try pressing next */
    const isLast = await page.evaluate(() => {
      let element = document.querySelector('ul.numbers > li:last-child')
      // @ts-ignore
      if (parseInt(element.innerText) == NaN) {
        return true
      }
      return false
    })

    /* We reached the last page */
    if (isLast) break

    await page.click('ul.numbers > li:last-child')
  }

  console.log('Loaded all data...')

  await browser.close()
})()
